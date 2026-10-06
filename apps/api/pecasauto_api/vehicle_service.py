from __future__ import annotations

from dataclasses import dataclass

from app.cascades import configured_registration_cascade, configured_vin_cascade
from app.models import EvidenceStatus, IdentityResult, LookupStatus, PrecisionLevel, VehicleCandidate
from app.normalization import normalize_pt_registration, normalize_vin

from .config import Settings
from .schemas import TraceStep, VehicleCandidateOut, VehicleSearchRequest, VehicleSearchResponse


@dataclass
class VehicleIdentificationService:
    settings: Settings

    def search(self, request: VehicleSearchRequest) -> VehicleSearchResponse:
        value = request.value.strip().upper()
        if request.method == "registration":
            value = normalize_pt_registration(value)
        else:
            parsed = normalize_vin(value)
            if not parsed.structurally_valid:
                return self._invalid(request.method, value, "VIN inválido. Confirme os 17 caracteres.")
            value = parsed.normalized

        selected, attempts = self._run_provider_cascade(request.method, value)
        useful = selected or self._best_partial(attempts)
        if useful is not None:
            return self._from_provider_evidence(request.method, value, useful, attempts)

        message = (
            "WAITING_FOR_PROVIDER — a camada de identificação está pronta, mas nenhuma fonte live de matrícula está ligada. Use a seleção manual."
            if request.method == "registration"
            else "WAITING_FOR_PROVIDER — o fornecedor VIN gratuito não devolveu identidade útil e nenhuma fonte comercial live está ligada. Use a seleção manual."
        )
        return VehicleSearchResponse(
            outcome="WAITING_FOR_PROVIDER",
            source_type="WAITING_FOR_ACCESS",
            input={"method": request.method, "value": value},
            candidates=[],
            trace=[self._trace_from_result(item) for item in attempts],
            message=message,
        )

    def demo_conflict(self) -> VehicleSearchResponse:
        """Neutral canned data used only to demonstrate the confirmation UI."""
        candidates = [
            VehicleCandidateOut(
                id="demo-golf-16-tdi", make="Volkswagen", model="Golf", generation="VII",
                year_range="2017–2020", engine="1.6 TDI 110", power_kw=81, fuel="Diesel",
                provider="PeçasAuto canned demo scenario", precision="ENGINE",
                verification_state="DEMO_CANNED_NEEDS_USER_CONFIRMATION",
            ),
            VehicleCandidateOut(
                id="demo-golf-20-tdi", make="Volkswagen", model="Golf", generation="VII",
                year_range="2017–2020", engine="2.0 TDI 150", power_kw=110, fuel="Diesel",
                provider="PeçasAuto canned demo scenario", precision="ENGINE",
                verification_state="DEMO_CANNED_NEEDS_USER_CONFIRMATION",
            ),
        ]
        return VehicleSearchResponse(
            outcome="MULTIPLE", source_type="DEMO",
            input={"method": "demo", "value": "CANNED-CONFLICT-SCENARIO"},
            candidates=candidates,
            trace=[TraceStep(provider="PeçasAuto canned demo dataset", status="DEMO CANNED RESULT", detail="No external provider was called.", source_type="DEMO")],
            raw_provider_result={"label": "DEMO CANNED RESULT", "external_call": False},
            message="DEMO CANNED RESULT — nenhuma consulta externa foi feita. Escolha uma versão para demonstrar a confirmação manual.",
        )

    def _run_provider_cascade(self, method: str, value: str) -> tuple[IdentityResult | None, list[IdentityResult]]:
        cascade = configured_vin_cascade() if method == "vin" else configured_registration_cascade()
        return cascade.identify(method, value)

    @staticmethod
    def _best_partial(attempts: list[IdentityResult]) -> IdentityResult | None:
        usable = [
            item for item in attempts
            if item.candidates and item.status not in {LookupStatus.ERROR, LookupStatus.NO_RESULT, LookupStatus.NOT_CONFIGURED}
        ]
        return max(usable, key=lambda item: item.best_precision, default=None)

    def _from_provider_evidence(self, method: str, value: str, result: IdentityResult, attempts: list[IdentityResult]) -> VehicleSearchResponse:
        candidates = [
            self._candidate_from_domain(
                item,
                result.provider,
                validated=result.evidence_status is EvidenceStatus.VERIFIED,
            )
            for item in result.candidates
        ]
        disagreements = self._provider_disagreements(attempts)
        if disagreements:
            outcome = "CONFLICT"
            message = "Conflito entre fornecedores. É necessária confirmação do utilizador ou uma segunda fonte."
        elif len(candidates) > 1:
            outcome = "MULTIPLE"
            message = "Encontrámos várias versões possíveis. Confirme o seu veículo."
        elif result.best_precision < PrecisionLevel.ENGINE:
            outcome = "MORE_INFORMATION_REQUIRED"
            message = "Encontrámos parte da viatura, mas falta confirmar motor e versão."
        elif result.evidence_status is not EvidenceStatus.VERIFIED:
            outcome = "MORE_INFORMATION_REQUIRED"
            message = "Resultado de fornecedor não verificado. Confirme a versão ou obtenha uma segunda fonte."
        else:
            outcome = "EXACT"
            message = "Viatura identificada por uma fonte testada. Confirme antes de guardar."
        source_type = "REAL_TESTED" if result.candidates and result.status is not LookupStatus.NOT_CONFIGURED else "WAITING_FOR_ACCESS"
        return VehicleSearchResponse(
            outcome=outcome, source_type=source_type,
            input={"method": method, "value": value}, candidates=candidates,
            trace=[self._trace_from_result(item) for item in attempts],
            raw_provider_result={
                "status": result.status.value, "provider": result.provider,
                "candidate_count": len(result.candidates),
                "raw_payload_reference": result.raw_payload_ref,
                "display_note": "Raw payload is not persisted by the customer application unless provider terms allow it.",
            },
            message=message, may_claim_compatibility=False,
        )

    @staticmethod
    def _provider_disagreements(attempts: list[IdentityResult]) -> list[str]:
        provider_candidates = [attempt.candidates for attempt in attempts if attempt.candidates]
        if len(provider_candidates) < 2:
            return []
        disagreements: list[str] = []
        for field in ("make", "model", "engine_code"):
            values_by_provider = [
                {
                    str(getattr(candidate, field)).strip().casefold()
                    for candidate in candidates
                    if getattr(candidate, field)
                }
                for candidates in provider_candidates
            ]
            populated = [values for values in values_by_provider if values]
            if len(populated) >= 2 and not set.intersection(*populated):
                disagreements.append(field)
        return disagreements

    @staticmethod
    def _candidate_from_domain(candidate: VehicleCandidate, provider: str, *, validated: bool) -> VehicleCandidateOut:
        ktype = candidate.provider_vehicle_ids.get("ktype") or candidate.provider_vehicle_ids.get("autoways_ktype")
        external_id = candidate.provider_vehicle_ids.get("provider_id")
        year = candidate.model_year or candidate.first_registration_year
        return VehicleCandidateOut(
            id=f"{provider}-{external_id or candidate.vin or 'candidate'}",
            make=candidate.make, model=candidate.model, generation=candidate.generation,
            year_range=str(year) if year else None, engine=candidate.engine_family,
            engine_code=candidate.engine_code, power_kw=candidate.power_kw, fuel=candidate.fuel,
            variant=candidate.variant, provider=provider, external_vehicle_id=external_id,
            ktype=ktype, ktype_status="UNVERIFIED" if ktype else "NOT_AVAILABLE",
            precision=(
                PrecisionLevel.ENGINE.name
                if candidate.precision is PrecisionLevel.EXACT_VARIANT and not validated
                else candidate.precision.name
            ),
            verification_state="NEEDS_SECOND_SOURCE_OR_USER_CONFIRMATION",
        )

    @staticmethod
    def _trace_from_result(result: IdentityResult | None) -> TraceStep:
        if result is None:
            return TraceStep(provider="none", status="NOT_CONFIGURED", detail="Nenhum resultado de fornecedor.", source_type="NOT_CONFIGURED")
        if result.candidates and result.status is not LookupStatus.NOT_CONFIGURED:
            source_type = "REAL_TESTED"
        elif result.evidence_status is EvidenceStatus.WAITING_FOR_CREDENTIALS:
            source_type = "WAITING_FOR_ACCESS"
        else:
            source_type = "NOT_CONFIGURED"
        return TraceStep(
            provider=result.provider, status=result.status.value,
            detail=result.error_code or f"{len(result.candidates)} candidato(s)",
            source_type=source_type, latency_ms=result.latency_ms,
        )

    @staticmethod
    def _invalid(method: str, value: str, message: str) -> VehicleSearchResponse:
        return VehicleSearchResponse(outcome="NO_RESULT", source_type="NOT_CONFIGURED", input={"method": method, "value": value}, candidates=[], trace=[], message=message)


MANUAL_VEHICLES = {
    "Volkswagen": {"Caddy": {"III": {"2008": ["1.9 TDI 77 kW", "2.0 SDI 51 kW"]}}},
    "Peugeot": {"5008": {"II": {"2023": ["1.5 BlueHDi 130", "1.2 PureTech 130"]}}, "3008": {"II": {"2023": ["1.5 BlueHDi 130", "1.2 PureTech 130"]}}},
    "Renault": {"Clio": {"V": {"2022": ["1.0 TCe 90", "1.5 Blue dCi 100"]}}},
    "Citroën": {"C3": {"III": {"2021": ["1.2 PureTech 83", "1.5 BlueHDi 100"]}}},
    "Mercedes-Benz": {"Classe A": {"W177": {"2021": ["A 180 d", "A 200"]}}},
    "BMW": {"Série 3": {"G20": {"2021": ["318d", "320i"]}}},
    "Audi": {"A3": {"8Y": {"2021": ["30 TDI", "35 TFSI"]}}},
    "SEAT": {"Leon": {"KL": {"2021": ["1.0 TSI 110", "2.0 TDI 150"]}}},
    "Skoda": {"Octavia": {"NX": {"2021": ["1.0 TSI 110", "2.0 TDI 150"]}}},
    "Opel": {"Corsa": {"F": {"2021": ["1.2 75", "1.5 Diesel 100"]}}},
    "Ford": {"Focus": {"IV": {"2021": ["1.0 EcoBoost 125", "1.5 EcoBlue 120"]}}},
    "Toyota": {"Corolla": {"E210": {"2021": ["1.8 Hybrid", "2.0 Hybrid"]}}},
    "Fiat": {"500": {"312": {"2020": ["1.2 69", "1.0 Hybrid 70"]}}},
}
