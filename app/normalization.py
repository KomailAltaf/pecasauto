from __future__ import annotations

import re
from dataclasses import dataclass


VIN_WEIGHTS = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
VIN_VALUES = {**{str(i): i for i in range(10)}}
for chars, value in [("AJS", 1), ("BKT", 2), ("CLU", 3), ("DMV", 4), ("ENW", 5), ("FPX", 6), ("GY", 7), ("HZ", 8), ("R", 9)]:
    VIN_VALUES.update({char: value for char in chars})


@dataclass(frozen=True)
class VINValidation:
    normalized: str
    structurally_valid: bool
    checksum_applicable: bool
    checksum_valid: bool | None
    warnings: tuple[str, ...]


def normalize_vin(value: str, region: str = "EU") -> VINValidation:
    normalized = re.sub(r"[\s-]", "", value).upper()
    structural = len(normalized) == 17 and not re.search(r"[IOQ]", normalized) and normalized.isalnum()
    warnings: list[str] = []
    applicable = region.upper() in {"NA", "US", "CA", "MX", "CN"}
    checksum = vin_checksum_valid(normalized) if structural else None
    if structural and checksum is False and not applicable:
        warnings.append("CHECKSUM_MISMATCH_NON_BLOCKING_FOR_REGION")
    if not structural:
        warnings.append("INVALID_VIN_STRUCTURE")
    return VINValidation(normalized, structural, applicable, checksum, tuple(warnings))


def vin_checksum_valid(vin: str) -> bool | None:
    if len(vin) != 17 or any(char not in VIN_VALUES for char in vin):
        return None
    total = sum(VIN_VALUES[char] * weight for char, weight in zip(vin, VIN_WEIGHTS))
    expected = "X" if total % 11 == 10 else str(total % 11)
    return vin[8] == expected


PT_PATTERNS = (
    re.compile(r"^\d{2}\d{2}[A-Z]{2}$"),
    re.compile(r"^\d{2}[A-Z]{2}\d{2}$"),
    re.compile(r"^[A-Z]{2}\d{4}$"),
    re.compile(r"^[A-Z]{2}\d{2}[A-Z]{2}$"),
)


def normalize_pt_registration(value: str) -> str:
    compact = re.sub(r"[^A-Za-z0-9]", "", value).upper()
    if len(compact) != 6 or not any(pattern.match(compact) for pattern in PT_PATTERNS):
        raise ValueError("not a supported Portuguese registration format")
    return "-".join((compact[:2], compact[2:4], compact[4:]))


def normalize_reference(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", value).upper()


def next_required_discriminator(candidate) -> str | None:
    for field in ("engine_family", "power_kw", "fuel", "variant"):
        if getattr(candidate, field, None) in (None, ""):
            return field
    return None

