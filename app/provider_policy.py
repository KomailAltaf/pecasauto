from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderPolicy:
    provider: str
    commercial_use_status: str = "UNKNOWN"
    cache_allowed: bool = False
    storage_allowed: bool = False
    cache_ttl_seconds: int = 0
    terms_verified: bool = False

    def __post_init__(self) -> None:
        if not self.terms_verified and (self.cache_allowed or self.storage_allowed or self.cache_ttl_seconds):
            raise ValueError("unverified terms cannot enable persistent caching or storage")
        if not self.cache_allowed and self.cache_ttl_seconds:
            raise ValueError("cache_ttl_seconds requires cache_allowed")

