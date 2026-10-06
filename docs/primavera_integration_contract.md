# Primavera / Cegid integration boundary

Primavera is the operational system for:

- stock by product and warehouse;
- customer-specific and public prices;
- customers;
- order creation/status;
- invoice creation/reference.

It is explicitly **not** responsible for vehicle identification, KType resolution or product fitment.

The code boundary is `ERPProvider`:

```text
get_stock(product_id) → StockRecord
get_price(product_id, customer_id?) → PriceRecord
upsert_customer(CustomerRecord) → IntegrationResult
create_order(OrderDraft) → OrderRecord
create_invoice(order_id) → InvoiceRecord
```

`PrimaveraERPProvider` currently returns `NOT_CONFIGURED`. Implementation must wait for inspection of the exact version, modules, API, authentication, stock locations, price lists, customer rules, order types and invoice workflow.

Phase 1 may use reviewed imports/exports or a controlled manual handoff. Phase 2 can add stock, price, order, invoice and customer synchronization after the operational contract is verified.
