from __future__ import annotations

import os

from .schemas import ProviderStatusOut


def provider_statuses() -> list[ProviderStatusOut]:
    configured = lambda key: bool(os.getenv(key))
    autoways_configured = configured("AUTOWAYS_API_KEY") or configured("AUTOWAYS_API_TOKEN")
    tips4y_configured = configured("TIPS4Y_API_KEY") and configured("TIPS4Y_BASE_URL")
    matriculapt_configured = configured("MATRICULAPT_USERNAME")
    telepecas_configured = configured("TELEPECAS_ACCESS_TOKEN") or (configured("TELEPECAS_CLIENT_ID") and configured("TELEPECAS_CLIENT_SECRET"))
    return [
        ProviderStatusOut(
            name="Free VIN / vPIC", role="VIN básico / routing", status="TESTED",
            registration=False, vin=True, ktype=False, catalogue=False, fitment=False, inventory=False,
            approximate_cost="Gratuito", note="Testado no VIN português fornecido; devolveu apenas nível BASIC.",
            evidence_state="TESTED", tested_inputs=["VIN"], capability_basis="ACTUAL TEST",
        ),
        ProviderStatusOut(
            name="Auto Ways", role="Identificação por VIN e matrícula",
            status="NOT CONFIGURED" if not autoways_configured else "CONNECTED — TEST REQUIRED",
            registration=True, vin=True, ktype=True, catalogue=False, fitment=False, inventory=False,
            approximate_cost="TO CONFIRM", note="Capacidade baseada em documentação. Nenhuma resposta real é apresentada como evidência no demo.",
            evidence_state="NOT CONFIGURED" if not autoways_configured else "DOCUMENTED CAPABILITY",
            tested_inputs=[], capability_basis="VENDOR DOCUMENTATION",
        ),
        ProviderStatusOut(
            name="TIPS4Y", role="Identidade + ponte para catálogo", status="CONNECTED — TEST REQUIRED" if tips4y_configured else "DOCUMENTED ONLY",
            registration=True, vin=True, ktype=True, catalogue=True, fitment=True, inventory=False,
            approximate_cost="TO CONFIRM", note="Capacidade documentada; sem resposta real.",
            evidence_state="DOCUMENTED CAPABILITY", tested_inputs=[], capability_basis="VENDOR DOCUMENTATION",
        ),
        ProviderStatusOut(
            name="Matricula.co.pt", role="Matrícula portuguesa", status="CONNECTED — TEST REQUIRED" if matriculapt_configured else "NOT CONFIGURED",
            registration=True, vin=False, ktype=False, catalogue=False, fitment=False, inventory=False,
            approximate_cost="Preço público por consulta; contrato por confirmar", note="Conta/API de teste necessária.",
            evidence_state="DOCUMENTED CAPABILITY" if matriculapt_configured else "NOT CONFIGURED", tested_inputs=[], capability_basis="VENDOR DOCUMENTATION",
        ),
        ProviderStatusOut(
            name="TelePeças", role="Identificação e catálogo local", status="CONNECTED — TEST REQUIRED" if telepecas_configured else "DOCUMENTED ONLY",
            registration=True, vin=True, ktype=True, catalogue=True, fitment=False, inventory=False,
            approximate_cost="UNKNOWN", note="API e direitos comerciais por confirmar.",
            evidence_state="DOCUMENTED CAPABILITY", tested_inputs=[], capability_basis="VENDOR DOCUMENTATION",
        ),
        ProviderStatusOut(
            name="Autofrance public lookup", role="Pesquisa manual / cross-check", status="RESEARCH ONLY",
            registration=False, vin=True, ktype=True, catalogue=False, fitment=False, inventory=False,
            approximate_cost="N/A", note="Não licenciado para produção; excluído da cascata de produção.",
            evidence_state="RESEARCH ONLY", tested_inputs=[], capability_basis="RESEARCH",
        ),
        ProviderStatusOut(
            name="partslink24", role="Validação manual / referências OE", status="MANUAL ONLY",
            registration=False, vin=True, ktype=False, catalogue=True, fitment=False, inventory=False,
            approximate_cost="Conta existente do cliente", note="Sem scraping; integração só com direitos escritos.",
            evidence_state="MANUAL ONLY", tested_inputs=[], capability_basis="CONTRACT/ACCOUNT",
        ),
        ProviderStatusOut(
            name="TecDoc / TecAlliance", role="Catálogo e fitment licenciados", status="WAITING FOR ACCESS",
            registration=True, vin=True, ktype=True, catalogue=True, fitment=True, inventory=False,
            approximate_cost="QUOTE REQUIRED", note="Capacidade documentada; nenhuma integração live.",
            evidence_state="DOCUMENTED CAPABILITY", tested_inputs=[], capability_basis="VENDOR DOCUMENTATION",
        ),
        ProviderStatusOut(
            name="Primavera / Cegid", role="ERP operacional", status="FUTURE",
            registration=False, vin=False, ktype=False, catalogue=False, fitment=False, inventory=True,
            approximate_cost="TO CONFIRM", note="Stock, preços, clientes, encomendas e faturas — não identidade.",
            evidence_state="FUTURE", tested_inputs=[], capability_basis="PLACEHOLDER",
        ),
        ProviderStatusOut(
            name="GLS", role="Expedição e tracking", status="NOT CONFIGURED",
            registration=False, vin=False, ktype=False, catalogue=False, fitment=False, inventory=False,
            approximate_cost="CONTRACT DEPENDENT", note="Timing e preço apresentados são DEMO; sem chamada live.",
            evidence_state="NOT CONFIGURED", tested_inputs=[], capability_basis="PLACEHOLDER",
        ),
    ]
