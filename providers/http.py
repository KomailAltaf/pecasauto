from __future__ import annotations

import json
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any

from app.models import EvidenceStatus, IdentityResult, LookupStatus


@dataclass(frozen=True)
class HTTPResponse:
    status: int
    body: bytes
    latency_ms: float
    content_type: str | None = None

    def json(self) -> Any:
        return json.loads(self.body.decode("utf-8"))


def http_request(
    method: str,
    url: str,
    *,
    query: dict[str, str] | None = None,
    headers: dict[str, str] | None = None,
    form: dict[str, str] | None = None,
    timeout: float = 20,
) -> HTTPResponse:
    if query:
        separator = "&" if "?" in url else "?"
        url = url + separator + urllib.parse.urlencode(query)
    body = urllib.parse.urlencode(form).encode() if form else None
    request_headers = {"Accept": "application/json", "User-Agent": "portugal-auto-validation-lab/0.2"}
    request_headers.update(headers or {})
    if form:
        request_headers["Content-Type"] = "application/x-www-form-urlencoded"
    request = urllib.request.Request(url, data=body, headers=request_headers, method=method)
    started = time.perf_counter()
    try:
        try:
            import certifi
            tls_context = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            tls_context = ssl.create_default_context()
        with urllib.request.urlopen(request, timeout=timeout, context=tls_context) as response:
            raw = response.read()
            return HTTPResponse(
                response.status,
                raw,
                (time.perf_counter() - started) * 1000,
                response.headers.get("Content-Type"),
            )
    except urllib.error.HTTPError as exc:
        raw = exc.read()
        return HTTPResponse(
            exc.code,
            raw,
            (time.perf_counter() - started) * 1000,
            exc.headers.get("Content-Type") if exc.headers else None,
        )


def not_configured(provider: str, reason: str) -> IdentityResult:
    return IdentityResult(
        provider,
        LookupStatus.NOT_CONFIGURED,
        evidence_status=EvidenceStatus.NOT_CONFIGURED,
        error_code=f"NOT_CONFIGURED:{reason}",
    )


def response_error(provider: str, response: HTTPResponse, raw_ref: str | None = None) -> IdentityResult:
    if response.status in {401, 403}:
        code = "AUTHORIZATION"
    elif response.status == 429:
        code = "RATE_LIMIT"
    elif response.status >= 500:
        code = "PROVIDER_ERROR"
    else:
        code = f"HTTP_{response.status}"
    return IdentityResult(
        provider,
        LookupStatus.ERROR,
        evidence_status=EvidenceStatus.NOT_VERIFIED,
        latency_ms=response.latency_ms,
        error_code=code,
        raw_payload_ref=raw_ref,
    )
