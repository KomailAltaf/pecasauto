from __future__ import annotations

import secrets
from dataclasses import dataclass

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .config import Settings


security = HTTPBasic(auto_error=False)


@dataclass(frozen=True)
class Principal:
    username: str
    role: str


def _authenticate(credentials: HTTPBasicCredentials | None, allowed_roles: set[str]) -> Principal:
    settings = Settings.from_env()
    configured = {
        "customer": (settings.customer_username, settings.customer_password),
        "admin": (settings.admin_username, settings.admin_password),
    }
    if credentials is not None:
        for role in allowed_roles:
            username, password = configured[role]
            if username and password and secrets.compare_digest(credentials.username, username) and secrets.compare_digest(credentials.password, password):
                return Principal(username=username, role=role)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Autenticação necessária.",
        headers={"WWW-Authenticate": "Basic"},
    )


def require_customer(credentials: HTTPBasicCredentials | None = Depends(security)) -> Principal:
    return _authenticate(credentials, {"customer", "admin"})


def require_admin(credentials: HTTPBasicCredentials | None = Depends(security)) -> Principal:
    return _authenticate(credentials, {"admin"})
