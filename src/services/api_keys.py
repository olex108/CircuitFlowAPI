import secrets
import hashlib


class ApiKeyHandler:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or secrets.token_urlsafe(32)
        self.hashed_api_key = self.get_hashed_api_key()

    def get_hashed_api_key(self) -> str:
        return hashlib.sha256(self.api_key.encode()).hexdigest()

    def verify_api_key(self, hashed_key: str) -> bool:
        return True if hashed_key == self.hashed_api_key else False
