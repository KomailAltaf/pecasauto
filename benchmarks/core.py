from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ALLOWED_TRUTH_CLASSES = {"CLIENT_PROVIDED", "INDEPENDENTLY_VERIFIED"}


def is_portuguese_market(row: dict[str, str]) -> bool:
    return row.get("country") == "PT" and row.get("portuguese_market_verified", "").lower() == "true"


def is_production_score_eligible(row: dict[str, str]) -> bool:
    """Production accuracy needs PT context and independently verified truth.

    Client-provided records are valid campaign inputs, but cannot independently prove
    that a provider is correct.
    """
    return is_portuguese_market(row) and row.get("truth_class") == "INDEPENDENTLY_VERIFIED"


def load_ground_truth(path: Path, include_synthetic: bool = False) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if include_synthetic:
        return rows
    return [row for row in rows if is_production_score_eligible(row)]


def load_campaign_inputs(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return [
        row for row in rows
        if row.get("country") == "PT" and row.get("truth_class") in ALLOWED_TRUTH_CLASSES
    ]


@dataclass(frozen=True)
class ProviderSummary:
    provider: str
    route: str
    status: str
    verified_n: int
    mock_n: int
    correct_vehicle: int | None = None
    correct_engine: int | None = None
    correct_variant: int | None = None
    ambiguous: int | None = None
    wrong: int | None = None
    no_result: int | None = None
    p50_latency_ms: float | None = None
    p95_latency_ms: float | None = None
    monthly_cost_10k: float | None = None
    commercial_rights: str = "UNKNOWN"
    note: str = ""


def provider_summaries() -> list[ProviderSummary]:
    return [
        ProviderSummary("Local VIN structural parser", "VIN", "PARTIALLY VERIFIED", 0, 0, note="Actual test n=1. Structure and non-blocking EU checksum only; no vehicle identity."),
        ProviderSummary("Autofrance public VIN", "VIN → KType", "PARTIALLY VERIFIED", 0, 0, correct_vehicle=None, correct_engine=None, correct_variant=0, ambiguous=1, wrong=None, no_result=0, p50_latency_ms=3916.2, p95_latency_ms=3916.2, monthly_cost_10k=0.0, commercial_rights="RESEARCH ONLY; PRODUCTION RIGHTS UNKNOWN", note="Actual test n=1. ENGINE-level result + KType 130708; KType identity cross-checked, VIN mapping partial, client model disputed, no existence check."),
        ProviderSummary("NHTSA vPIC public", "VIN", "PARTIALLY VERIFIED", 0, 0, correct_vehicle=None, correct_engine=None, correct_variant=None, ambiguous=0, wrong=None, no_result=0, p50_latency_ms=874.3, p95_latency_ms=874.3, monthly_cost_10k=0.0, commercial_rights="PUBLIC API", note="Actual test n=1 without independent truth: make only, BASIC_ONLY; not fit for PT automatic identity."),
        ProviderSummary("Self-hosted vPIC", "VIN", "PARTIALLY VERIFIED", 0, 0, correct_vehicle=None, correct_engine=None, correct_variant=None, ambiguous=0, wrong=None, no_result=0, p50_latency_ms=162.8, p95_latency_ms=162.8, monthly_cost_10k=0.0, commercial_rights="MIT CODE / NHTSA DATA", note="Actual test n=1 without independent truth; reproduces public vPIC BASIC result and is not an independent source."),
        ProviderSummary("Mock identity provider", "VIN / matrícula", "MOCK ONLY", 0, 1, note="Plumbing and report mechanics only."),
        ProviderSummary("Existing client vehicle software", "matrícula / VIN", "NOT VERIFIED", 0, 0, note="Product and export/API capabilities not documented."),
        ProviderSummary("TelePeças", "matrícula / VIN", "WAITING FOR CREDENTIALS", 0, 0, note="Documentation, credentials, rights and price sheet required."),
        ProviderSummary("Matricula.co.pt", "matrícula", "WAITING FOR CREDENTIALS", 0, 0, note="Test credentials, terms and response schema required."),
        ProviderSummary("Openapi PT-car", "matrícula", "NOT VERIFIED", 0, 0, monthly_cost_10k=4000.0, commercial_rights="DOCUMENTED B2B; TERMS TO VERIFY", note="Portugal endpoint and pricing documented; no real response tested."),
        ProviderSummary("Tips4y matrícula", "matrícula → KType", "NOT VERIFIED", 0, 0, commercial_rights="CONTRACT REQUIRED", note="Portugal plate/VIN/KType bridge documented; no credentials or response."),
        ProviderSummary("Commercial VIN provider", "VIN", "NOT VERIFIED", 0, 0, note="Candidate not selected."),
        ProviderSummary("TecAlliance / TecDoc", "VIN / VRM / catalogue / fitment", "WAITING FOR CREDENTIALS", 0, 0, note="Direct consultation and licence required."),
        ProviderSummary("partslink24", "VIN / OE validation", "WAITING FOR CREDENTIALS", 0, 0, commercial_rights="UNKNOWN", note="Manual client access confirmed; programmatic rights unknown."),
    ]


def cost_scenarios() -> list[dict[str, object]]:
    volumes = (1_000, 10_000, 50_000, 100_000)
    rows: list[dict[str, object]] = []
    for provider in provider_summaries():
        for cache_policy in ("CACHE_ALLOWED", "CACHE_FORBIDDEN"):
            for volume in volumes:
                rows.append({
                    "provider": provider.provider,
                    "monthly_lookups": volume,
                    "cache_policy": cache_policy,
                    "status": provider.status,
                    "fixed_fee": None,
                    "per_call_fee": None,
                    "estimated_cost": 0.0 if provider.provider in {"Local VIN structural parser", "Autofrance public VIN", "NHTSA vPIC public", "Self-hosted vPIC"} else None,
                    "cost_per_successful": None,
                    "cost_per_engine": None,
                    "cost_per_exact_variant": None,
                    "note": "No provider price sheet or measured cascade pass-through rate is stored.",
                })
    return rows
