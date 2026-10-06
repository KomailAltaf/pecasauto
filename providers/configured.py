from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Mapping

from app.models import EvidenceStatus, IdentityResult, LookupStatus, VehicleCandidate
from providers.base import VehicleIdentityProvider
from providers.http import HTTPResponse, not_configured, response_error


@dataclass(frozen=True)
class RouteRequest:
    method: str
    url: str
    query: dict[str, str]
    headers: dict[str, str]
    form: dict[str, str] | None = None


class ConfiguredVehicleProvider(VehicleIdentityProvider):
    """Shared adapter lifecycle. Concrete providers own request shape and parsing."""

    estimated_cost_per_call: float | None = None

    def __init__(self) -> None:
        self.last_raw: str | None = None
        self.last_content_type: str | None = None
        self.last_http_status: int | None = None

    @property
    def configuration_error(self) -> str | None:
        raise NotImplementedError

    def configuration_error_for_route(self, route: str) -> str | None:
        return self.configuration_error

    def build_request(self, route: str, value: str) -> RouteRequest:
        raise NotImplementedError

    def execute(self, request: RouteRequest) -> HTTPResponse:
        from providers.http import http_request

        return http_request(
            request.method,
            request.url,
            query=request.query,
            headers=request.headers,
            form=request.form,
        )

    def parse_response(self, route: str, value: str, response: HTTPResponse) -> list[VehicleCandidate]:
        raise NotImplementedError

    def _identify(self, route: str, value: str) -> IdentityResult:
        configuration_error = self.configuration_error_for_route(route)
        if configuration_error:
            return not_configured(self.name, configuration_error)
        try:
            request = self.build_request(route, value)
            response = self.execute(request)
        except NotImplementedError as exc:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code=f"UNSUPPORTED_ROUTE:{exc}")
        except ValueError as exc:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code=f"INVALID_INPUT:{exc}")
        except PermissionError:
            return IdentityResult(self.name, LookupStatus.ERROR, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code="AUTHORIZATION")
        except TimeoutError:
            return IdentityResult(self.name, LookupStatus.ERROR, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code="TIMEOUT")
        except OSError as exc:
            return IdentityResult(self.name, LookupStatus.ERROR, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code=f"NETWORK_ERROR:{type(exc).__name__}")
        self.last_raw = response.body.decode("utf-8", errors="replace")
        self.last_content_type = response.content_type
        self.last_http_status = response.status
        if not 200 <= response.status < 300:
            return response_error(self.name, response)
        try:
            candidates = [
                candidate for candidate in self.parse_response(route, value, response)
                if candidate.make or candidate.model or candidate.vin or candidate.provider_vehicle_ids
            ]
        except (ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            return IdentityResult(
                self.name,
                LookupStatus.ERROR,
                evidence_status=EvidenceStatus.NOT_VERIFIED,
                latency_ms=response.latency_ms,
                cost=self.estimated_cost_per_call,
                error_code=f"SCHEMA_ERROR:{type(exc).__name__}",
            )
        if not candidates:
            status = LookupStatus.NO_RESULT
        elif len(candidates) > 1 or any(candidate.ambiguity for candidate in candidates):
            status = LookupStatus.AMBIGUOUS
        elif candidates[0].precision.value >= 3:
            status = LookupStatus.RESOLVED
        else:
            status = LookupStatus.PARTIAL
        for candidate in candidates:
            candidate.candidate_count = len(candidates)
            candidate.ambiguity = len(candidates) > 1
        return IdentityResult(
            self.name,
            status,
            candidates,
            EvidenceStatus.NOT_VERIFIED,
            latency_ms=response.latency_ms,
            cost=self.estimated_cost_per_call,
        )

    def identify_by_vin(self, vin: str) -> IdentityResult:
        return self._identify("vin", vin)

    def identify_by_registration(self, registration: str) -> IdentityResult:
        return self._identify("registration", registration)
