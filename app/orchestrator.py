from __future__ import annotations

from dataclasses import dataclass

from app.models import IdentityResult, LookupStatus, PrecisionLevel
from providers.base import VehicleIdentityProvider


class ProviderRateLimitError(RuntimeError):
    pass


class ProviderSchemaError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProviderStep:
    provider: VehicleIdentityProvider
    min_precision: PrecisionLevel
    max_cost: float | None = None


class ProviderScopedCache:
    def __init__(self):
        self._values: dict[tuple[str, str, str, str], IdentityResult] = {}

    def get(self, provider: VehicleIdentityProvider, route: str, value: str):
        return self._values.get((provider.name, provider.version, route, value))

    def put(self, provider: VehicleIdentityProvider, route: str, value: str, result: IdentityResult):
        self._values[(provider.name, provider.version, route, value)] = result


class IdentityOrchestrator:
    def __init__(self, steps: list[ProviderStep], failure_threshold: int = 2):
        self.steps = steps
        self.failure_threshold = failure_threshold
        self.failures: dict[str, int] = {}
        self.cache = ProviderScopedCache()

    def identify(self, route: str, value: str) -> tuple[IdentityResult | None, list[IdentityResult]]:
        attempts: list[IdentityResult] = []
        for step in self.steps:
            provider = step.provider
            if self.failures.get(provider.name, 0) >= self.failure_threshold:
                attempts.append(IdentityResult(provider.name, LookupStatus.ERROR, error_code="CIRCUIT_OPEN"))
                continue
            cached = self.cache.get(provider, route, value)
            if cached:
                result = cached
            else:
                try:
                    method = provider.identify_by_vin if route == "vin" else provider.identify_by_registration
                    result = method(value)
                    self.cache.put(provider, route, value, result)
                except TimeoutError:
                    self.failures[provider.name] = self.failures.get(provider.name, 0) + 1
                    result = IdentityResult(provider.name, LookupStatus.ERROR, error_code="TIMEOUT")
                except PermissionError:
                    self.failures[provider.name] = self.failures.get(provider.name, 0) + 1
                    result = IdentityResult(provider.name, LookupStatus.ERROR, error_code="AUTHORIZATION")
                except ProviderRateLimitError:
                    self.failures[provider.name] = self.failures.get(provider.name, 0) + 1
                    result = IdentityResult(provider.name, LookupStatus.ERROR, error_code="RATE_LIMIT")
                except ProviderSchemaError:
                    self.failures[provider.name] = self.failures.get(provider.name, 0) + 1
                    result = IdentityResult(provider.name, LookupStatus.ERROR, error_code="SCHEMA_DRIFT")
                except Exception:
                    self.failures[provider.name] = self.failures.get(provider.name, 0) + 1
                    result = IdentityResult(provider.name, LookupStatus.ERROR, error_code="MALFORMED_OR_PROVIDER_ERROR")
            attempts.append(result)
            cost_ok = step.max_cost is None or result.cost is None or result.cost <= step.max_cost
            if result.status is LookupStatus.RESOLVED and result.best_precision >= step.min_precision and cost_ok:
                return result, attempts
        return None, attempts
