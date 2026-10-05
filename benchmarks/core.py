from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


ALLOWED_TRUTH_CLASSES = {"CLIENT_PROVIDED", "INDEPENDENTLY_VERIFIED"}


def load_ground_truth(path: Path, include_synthetic: bool = False) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if include_synthetic:
        return rows
    return [row for row in rows if row["truth_class"] in ALLOWED_TRUTH_CLASSES]


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
        ProviderSummary("Local VIN structural parser", "VIN", "PARTIALLY VERIFIED", 1, 0, note="Structure and non-blocking EU checksum only; no vehicle identity."),
        ProviderSummary("Mock identity provider", "VIN / matrícula", "MOCK ONLY", 0, 1, note="Plumbing and report mechanics only."),
        ProviderSummary("Existing client vehicle software", "matrícula / VIN", "NOT VERIFIED", 0, 0, note="Product and export/API capabilities not documented."),
        ProviderSummary("TelePeças", "matrícula / VIN", "WAITING FOR CREDENTIALS", 0, 0, note="Documentation, credentials, rights and price sheet required."),
        ProviderSummary("Matricula.co.pt", "matrícula", "WAITING FOR CREDENTIALS", 0, 0, note="Test credentials, terms and response schema required."),
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
                    "status": "MOCK ONLY" if provider.status == "MOCK ONLY" else "WAITING FOR CREDENTIALS",
                    "fixed_fee": None,
                    "per_call_fee": None,
                    "estimated_cost": 0.0 if provider.provider == "Local VIN structural parser" else None,
                    "cost_per_successful": None,
                    "cost_per_engine": None,
                    "cost_per_exact_variant": None,
                    "note": "No provider price sheet or measured cascade pass-through rate is stored.",
                })
    return rows

