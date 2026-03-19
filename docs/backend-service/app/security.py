import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from .config import settings


INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "developer message",
    "<script",
    "BEGIN PRIVATE KEY",
]


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def issue_token() -> str:
    return base64.urlsafe_b64encode(os.urandom(24)).decode("utf-8").rstrip("=")


def _master_key() -> bytes:
    if not settings.master_key_b64:
        raise ValueError("MASTER_KEY_B64 missing")
    return base64.urlsafe_b64decode(settings.master_key_b64)


def encrypt_key(raw_key: str) -> str:
    key = _master_key()
    if len(key) != 32:
        raise ValueError("MASTER_KEY_B64 must decode to exactly 32 bytes")
    nonce = os.urandom(12)
    aes = AESGCM(key)
    ciphertext = aes.encrypt(nonce, raw_key.encode("utf-8"), None)
    return base64.urlsafe_b64encode(nonce + ciphertext).decode("utf-8")


def decrypt_key(encrypted: str) -> str:
    key = _master_key()
    if len(key) != 32:
        raise ValueError("MASTER_KEY_B64 must decode to exactly 32 bytes")
    raw = base64.urlsafe_b64decode(encrypted)
    nonce, ciphertext = raw[:12], raw[12:]
    aes = AESGCM(key)
    return aes.decrypt(nonce, ciphertext, None).decode("utf-8")


def contains_injection(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in INJECTION_PATTERNS)
