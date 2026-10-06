from __future__ import annotations

import os
from typing import Mapping

from app.integrations import CustomerRecord, IntegrationResult, InvoiceRecord, OrderDraft, OrderRecord, PriceRecord, StockRecord
from app.settings import env_value
from providers.base import ERPProvider


class PrimaveraERPProvider(ERPProvider):
    """Cegid/Primavera contract boundary; no vehicle or fitment operations."""

    name = "primavera"

    def __init__(self, *, base_url: str | None = None, api_key: str | None = None, env: Mapping[str, str] | None = None):
        source = env if env is not None else os.environ
        self.base_url = base_url or env_value("PRIMAVERA_BASE_URL", env=source)
        self.api_key = api_key or env_value("PRIMAVERA_API_KEY", env=source)

    @property
    def configuration_error(self) -> str | None:
        return None if self.base_url and self.api_key else "PRIMAVERA_BASE_URL and PRIMAVERA_API_KEY are required after version/API inspection"

    def _blocked(self) -> IntegrationResult:
        return IntegrationResult.not_configured(self.name, self.configuration_error or "Primavera implementation pending inspected API contract")

    def get_stock(self, product_id: str) -> StockRecord | IntegrationResult:
        return self._blocked()

    def get_price(self, product_id: str, customer_id: str | None = None) -> PriceRecord | IntegrationResult:
        return self._blocked()

    def upsert_customer(self, customer: CustomerRecord) -> IntegrationResult:
        return self._blocked()

    def create_order(self, order: OrderDraft) -> OrderRecord | IntegrationResult:
        return self._blocked()

    def create_invoice(self, order_id: str) -> InvoiceRecord | IntegrationResult:
        return self._blocked()
