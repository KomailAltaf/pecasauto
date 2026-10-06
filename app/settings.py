from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Mapping

from dotenv import load_dotenv


load_dotenv(override=False)


def _value(env: Mapping[str, str], key: str, default: str | None = None) -> str | None:
    value = env.get(key, default)
    return value.strip() if isinstance(value, str) and value.strip() else None


@dataclass(frozen=True)
class PlatformSettings:
    vehicle_provider: str = "autoways"
    fallback_provider: str = "matriculapt"
    catalogue_vehicle_provider: str = "tecdoc"
    fitment_provider: str = "tecdoc"
    inventory_provider: str = "primavera"
    supplier_provider: str = "none"
    erp_provider: str = "primavera"

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "PlatformSettings":
        source = env if env is not None else os.environ
        return cls(
            vehicle_provider=_value(source, "VEHICLE_PROVIDER", "autoways") or "autoways",
            fallback_provider=_value(source, "FALLBACK_PROVIDER", "matriculapt") or "matriculapt",
            catalogue_vehicle_provider=_value(source, "CATALOGUE_VEHICLE_PROVIDER", "tecdoc") or "tecdoc",
            fitment_provider=_value(source, "FITMENT_PROVIDER", "tecdoc") or "tecdoc",
            inventory_provider=_value(source, "INVENTORY_PROVIDER", "primavera") or "primavera",
            supplier_provider=_value(source, "SUPPLIER_PROVIDER", "none") or "none",
            erp_provider=_value(source, "ERP_PROVIDER", "primavera") or "primavera",
        )


def env_value(key: str, default: str | None = None, env: Mapping[str, str] | None = None) -> str | None:
    return _value(env if env is not None else os.environ, key, default)
