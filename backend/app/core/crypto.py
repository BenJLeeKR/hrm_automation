from cryptography.fernet import Fernet, InvalidToken

from app.core.config import settings


class ConfigEncryptionError(Exception):
    """`CONFIG_ENCRYPTION_KEY` 미설정 또는 복호화 실패를 감싸는 예외."""


def _get_fernet() -> Fernet:
    if not settings.CONFIG_ENCRYPTION_KEY:
        raise ConfigEncryptionError(
            "CONFIG_ENCRYPTION_KEY가 설정되지 않았습니다 — .env에 32바이트 base64 키를 지정해야 합니다."
        )
    try:
        return Fernet(settings.CONFIG_ENCRYPTION_KEY)
    except (ValueError, TypeError) as exc:
        raise ConfigEncryptionError("CONFIG_ENCRYPTION_KEY 형식이 올바르지 않습니다.") from exc


def encrypt_secret(plain_value: str) -> str:
    """`SYS_CONFIG.IS_SECRET=TRUE` 항목 저장 전 암호화 (설계서 §5.3.17)."""
    return _get_fernet().encrypt(plain_value.encode("utf-8")).decode("utf-8")


def decrypt_secret(encrypted_value: str) -> str:
    try:
        return _get_fernet().decrypt(encrypted_value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ConfigEncryptionError("암호화된 값을 복호화할 수 없습니다 — 키가 변경되었을 수 있습니다.") from exc
