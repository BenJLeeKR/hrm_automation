# SYS_CONFIG 초기 Seed — 알림 채널 그룹 (설계서 §5.3.17, 2026-07-05)
# CONFIG_VAL은 전부 NULL로 시작 — `.env`(TEAMS_WEBHOOK_URL 등)로 폴백하며, 관리자가
# `/settings/notification` 화면에서 값을 입력하면 DB 값이 우선한다.

SYS_CONFIG_SEED = [
    {
        "CONFIG_KEY": "notification.teams_webhook_url",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "Teams Webhook URL",
        "IS_SECRET": False,
        "CONFIG_DESC": "Teams Incoming Webhook URL — 미설정 시 .env의 TEAMS_WEBHOOK_URL 사용",
    },
    {
        "CONFIG_KEY": "notification.smtp_host",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "SMTP 호스트",
        "IS_SECRET": False,
        "CONFIG_DESC": "이메일 알림 발송용 SMTP 서버 호스트",
    },
    {
        "CONFIG_KEY": "notification.smtp_port",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "SMTP 포트",
        "IS_SECRET": False,
        "CONFIG_DESC": "이메일 알림 발송용 SMTP 포트 (기본값 587)",
    },
    {
        "CONFIG_KEY": "notification.smtp_user",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "SMTP 사용자",
        "IS_SECRET": False,
        "CONFIG_DESC": "SMTP 인증 사용자 ID",
    },
    {
        "CONFIG_KEY": "notification.smtp_password",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "SMTP 비밀번호",
        "IS_SECRET": True,
        "CONFIG_DESC": "SMTP 인증 비밀번호 — AES-256 암호화 저장",
    },
    {
        "CONFIG_KEY": "notification.email_from",
        "CONFIG_GRP": "NOTIFICATION",
        "CONFIG_NM": "발신 이메일 주소",
        "IS_SECRET": False,
        "CONFIG_DESC": "이메일 알림 발신자 주소",
    },
]
