"""ShueBank password hashing — PBKDF2-HMAC-SHA256 with legacy SHA-256 migration."""
import hashlib
import hmac
import os
import base64
from typing import Tuple

PBKDF2_ALGO = "sha256"
PBKDF2_ITERATIONS = 260_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_BYTES)
    dk = hashlib.pbkdf2_hmac(PBKDF2_ALGO, password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return "pbkdf2${}${}${}".format(
        PBKDF2_ITERATIONS,
        base64.b64encode(salt).decode("ascii"),
        base64.b64encode(dk).decode("ascii"),
    )


def _verify_pbkdf2(password: str, stored: str) -> bool:
    try:
        scheme, iters_s, salt_b64, hash_b64 = stored.split("$")
        if scheme != "pbkdf2":
            return False
        salt = base64.b64decode(salt_b64)
        expected = base64.b64decode(hash_b64)
        dk = hashlib.pbkdf2_hmac(PBKDF2_ALGO, password.encode("utf-8"), salt, int(iters_s))
        return hmac.compare_digest(dk, expected)
    except Exception:
        return False


def _verify_sha256_legacy(password: str, stored: str) -> bool:
    legacy = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return hmac.compare_digest(legacy, stored)


def verify_password(password: str, stored: str) -> Tuple[bool, bool]:
    if stored.startswith("pbkdf2$"):
        return _verify_pbkdf2(password, stored), False
    if _verify_sha256_legacy(password, stored):
        return True, True
    return False, False
