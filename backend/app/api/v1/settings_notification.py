from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import require_permission
from app.core.audit import record_audit
from app.core.config import settings as app_settings
from app.core.crypto import ConfigEncryptionError, decrypt_secret, encrypt_secret
from app.db.session import get_db
from app.models.sys_user_mst import SysUserMst
from app.repositories.sys_config import list_notification_configs, upsert_config_value
from app.schemas.sys_config import (
    NotificationSettingsOut,
    NotificationSettingsUpdate,
    NotificationTestRequest,
    NotificationTestResponse,
)
from app.services.email_notify import EmailNotifyError, send_test_email
from app.services.teams_notify import TeamsNotifyError, send_teams_message

router = APIRouter(prefix="/settings/notification", tags=["settings-notification"])

_TGT_TBL_NM = "SYS_CONFIG"
_MASK = "*****"
_ENV_FALLBACK = {
    "notification.teams_webhook_url": "TEAMS_WEBHOOK_URL",
    "notification.smtp_host": "SMTP_HOST",
    "notification.smtp_port": "SMTP_PORT",
    "notification.smtp_user": "SMTP_USER",
    "notification.email_from": "EMAIL_FROM",
}


def _resolve_value(config) -> str:
    """`CONFIG_VAL`이 NULL이면 `.env` 값으로 폴백한다 (설계서 §5.3.17 "폴백 정책")."""
    if config.CONFIG_VAL is not None:
        return config.CONFIG_VAL
    env_key = _ENV_FALLBACK.get(config.CONFIG_KEY)
    return getattr(app_settings, env_key, "") if env_key else ""


def _build_settings_out(db: Session) -> NotificationSettingsOut:
    values: dict[str, str] = {}
    for config in list_notification_configs(db):
        field = config.CONFIG_KEY.removeprefix("notification.")
        if config.IS_SECRET:
            values[field] = _MASK if config.CONFIG_VAL else ""
        else:
            values[field] = _resolve_value(config)
    return NotificationSettingsOut(**values)


@router.get("", response_model=NotificationSettingsOut, dependencies=[Depends(require_permission("settings_notification", "view"))])
def get_notification_settings(db: Session = Depends(get_db)) -> NotificationSettingsOut:
    """알림 채널 설정 조회 (SCR-017). `IS_SECRET=TRUE` 항목(`smtp_password`)은 값이 있으면
    `*****`로 마스킹해 반환한다."""
    return _build_settings_out(db)


@router.put("", response_model=NotificationSettingsOut)
def update_notification_settings(
    payload: NotificationSettingsUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: SysUserMst = Depends(require_permission("settings_notification", "update")),
) -> NotificationSettingsOut:
    """알림 채널 설정 저장 (SCR-017). `None`인 필드는 변경하지 않는다 — `smtp_password`를
    빈칸으로 두면(`None`) 기존 암호화 값이 유지된다(설계서 §5.5 "동작 정의")."""
    audit_after: dict[str, str] = {}
    for field, value in payload.model_dump(exclude_unset=True, exclude_none=True).items():
        config_key = f"notification.{field}"
        stored_value = encrypt_secret(value) if field == "smtp_password" else value
        upsert_config_value(db, config_key, stored_value, upd_user=current_user.USER_LGID)
        audit_after[field] = "[SECRET_UPDATED]" if field == "smtp_password" else value

    record_audit(
        db, request, current_user, act_cd="UPDATE", tgt_tbl_nm=_TGT_TBL_NM, aft_val_json=audit_after
    )
    return _build_settings_out(db)


@router.post("/test", response_model=NotificationTestResponse)
def test_notification_channel(
    payload: NotificationTestRequest,
    current_user: SysUserMst = Depends(require_permission("settings_notification", "admin")),
    db: Session = Depends(get_db),
) -> NotificationTestResponse:
    """알림 채널 테스트 발송 (SCR-017 "테스트 발송" 버튼). Teams는 저장된 Webhook URL(또는
    `.env` 폴백)로, 이메일은 저장된 SMTP 설정으로 관리자 본인 계정(`current_user.EMAIL_ADDR`)에
    테스트 메시지를 보낸다 — 화면 설계서에 수신자가 별도 명시되어 있지 않아 요청자 본인
    계정으로 발송하는 것이 가장 안전한 기본값이라 판단했다."""
    configs = {c.CONFIG_KEY: c for c in list_notification_configs(db)}

    if payload.channel == "teams":
        webhook_url = _resolve_value(configs["notification.teams_webhook_url"])
        if not webhook_url:
            return NotificationTestResponse(sent=False, message="Teams Webhook URL이 설정되지 않았습니다.")
        original = app_settings.TEAMS_WEBHOOK_URL
        app_settings.TEAMS_WEBHOOK_URL = webhook_url
        try:
            send_teams_message("HRM 시스템 알림 채널(Teams) 테스트 메시지입니다.")
        except TeamsNotifyError as exc:
            return NotificationTestResponse(sent=False, message=f"발송 실패: {exc}")
        finally:
            app_settings.TEAMS_WEBHOOK_URL = original
        return NotificationTestResponse(sent=True, message="테스트 메시지가 발송되었습니다.")

    if payload.channel == "email":
        smtp_host = _resolve_value(configs["notification.smtp_host"])
        smtp_port = _resolve_value(configs["notification.smtp_port"])
        smtp_user = _resolve_value(configs["notification.smtp_user"])
        email_from = _resolve_value(configs["notification.email_from"])
        encrypted_password = configs["notification.smtp_password"].CONFIG_VAL
        if not (smtp_host and smtp_port and email_from and (encrypted_password or app_settings.SMTP_PASSWORD)):
            return NotificationTestResponse(sent=False, message="SMTP 설정이 완전하지 않습니다.")
        try:
            smtp_password = decrypt_secret(encrypted_password) if encrypted_password else app_settings.SMTP_PASSWORD
            send_test_email(
                smtp_host=smtp_host,
                smtp_port=int(smtp_port),
                smtp_user=smtp_user,
                smtp_password=smtp_password,
                email_from=email_from,
                email_to=current_user.EMAIL_ADDR,
            )
        except (EmailNotifyError, ConfigEncryptionError, ValueError) as exc:
            return NotificationTestResponse(sent=False, message=f"발송 실패: {exc}")
        return NotificationTestResponse(sent=True, message="테스트 메시지가 발송되었습니다.")

    return NotificationTestResponse(sent=False, message="지원하지 않는 채널입니다 (teams|email만 지원).")
