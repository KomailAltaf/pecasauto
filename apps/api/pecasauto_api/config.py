from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Settings:
    demo_mode: bool = False
    database_url: str = f"sqlite:///{ROOT / 'apps/api/data/pecasauto.db'}"
    web_origin: str = "http://localhost:3000"
    customer_username: str = ""
    customer_password: str = ""
    admin_username: str = ""
    admin_password: str = ""

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            demo_mode=os.getenv("DEMO_MODE", "false").lower() in {"1", "true", "yes", "on"},
            database_url=os.getenv("DATABASE_URL", cls.database_url),
            web_origin=os.getenv("WEB_ORIGIN", cls.web_origin),
            customer_username=os.getenv("CUSTOMER_USERNAME", ""),
            customer_password=os.getenv("CUSTOMER_PASSWORD", ""),
            admin_username=os.getenv("ADMIN_USERNAME", ""),
            admin_password=os.getenv("ADMIN_PASSWORD", ""),
        )
