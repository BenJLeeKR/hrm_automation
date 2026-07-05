from pydantic import BaseModel

_MASK = "*****"


class NotificationSettingsOut(BaseModel):
    """`GET /api/v1/settings/notification` 응답 (SCR-017). `IS_SECRET=TRUE` 항목
    (`smtp_password`)은 값이 설정되어 있으면 `*****`로 마스킹하고, 미설정이면 빈 문자열을
    반환한다 — 설정 여부만 화면에서 구분할 수 있게 한다(설계서 §5.5 "동작 정의")."""

    teams_webhook_url: str
    smtp_host: str
    smtp_port: str
    smtp_user: str
    smtp_password: str
    email_from: str


class NotificationSettingsUpdate(BaseModel):
    """`PUT /api/v1/settings/notification` 요청. 각 필드는 `None`이면 변경하지 않고 기존 값을
    유지한다 — 특히 `smtp_password`를 빈칸으로 두고 저장하면 기존 암호화 값이 유지된다."""

    teams_webhook_url: str | None = None
    smtp_host: str | None = None
    smtp_port: str | None = None
    smtp_user: str | None = None
    smtp_password: str | None = None
    email_from: str | None = None


class NotificationTestRequest(BaseModel):
    channel: str  # "teams" | "email"


class NotificationTestResponse(BaseModel):
    sent: bool
    message: str
