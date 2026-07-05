import smtplib
from email.mime.text import MIMEText

_REQUEST_TIMEOUT_SECONDS = 10.0


class EmailNotifyError(Exception):
    """SMTP 발송 실패(연결/인증 오류 등)를 감싸는 예외."""


def send_test_email(
    *, smtp_host: str, smtp_port: int, smtp_user: str, smtp_password: str, email_from: str, email_to: str
) -> None:
    """알림 채널 설정 화면의 "이메일 테스트 발송" 버튼 (SCR-017). `teams_notify.send_teams_message`와
    달리 SMTP 설정이 전부 갖춰져 있어야만 호출되므로(호출부에서 사전 검증), 미설정 시 조용히
    건너뛰는 처리는 하지 않는다 — 값이 없으면 호출 자체를 하지 않는다."""
    message = MIMEText("HRM 시스템 알림 채널(SMTP) 테스트 메시지입니다.")
    message["Subject"] = "[HRM] 알림 채널 테스트 발송"
    message["From"] = email_from
    message["To"] = email_to

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=_REQUEST_TIMEOUT_SECONDS) as server:
            server.starttls()
            if smtp_user:
                server.login(smtp_user, smtp_password)
            server.sendmail(email_from, [email_to], message.as_string())
    except (smtplib.SMTPException, OSError) as exc:
        raise EmailNotifyError(f"이메일 알림 발송이 실패했습니다: {exc}") from exc
