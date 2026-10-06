"use client";

import Link from "next/link";
import { Minus, Plus, Trash2 } from "lucide-react";
import { useCart } from "@/components/CartProvider";
import { PartVisual } from "@/components/PartVisual";
import { shippingCost } from "@/lib/cart";

export default function CartPage() {
  const { lines, remove, setQuantity, subtotal } = useCart();
  const shipping = shippingCost(subtotal);
  const money = (value:number) => `${value.toFixed(2).replace(".", ",")} €`;
  return <>
    <section className="page-hero"><div className="container"><span className="eyebrow" style={{color:"#83d3ad"}}>A sua encomenda</span><h1>Carrinho</h1><p>Preço com IVA incluído. Expedição GLS demonstrativa.</p></div></section>
    <section className="section"><div className="container cart-layout"><div>{!lines.length ? <div className="form-card"><h2>O carrinho está vazio.</h2><p className="section-copy">Explore o catálogo e adicione uma peça.</p><Link className="btn" href="/catalogo">Abrir catálogo</Link></div> : lines.map(line => <div className="cart-line" key={line.product.id}><PartVisual kind={line.product.image_kind}/><div><strong>{line.product.brand}</strong><h3>{line.product.name}</h3><span className="reference">{line.product.manufacturer_reference}</span></div><div><button className="icon-btn" onClick={() => setQuantity(line.product.id, line.quantity - 1)}><Minus size={15}/></button> {line.quantity} <button className="icon-btn" onClick={() => setQuantity(line.product.id, line.quantity + 1)}><Plus size={15}/></button></div><strong>{money(line.product.price * line.quantity)}</strong><button className="icon-btn" onClick={() => remove(line.product.id)} aria-label="Remover"><Trash2 size={18}/></button></div>)}</div>
      <aside className="summary-card"><h2>Resumo</h2><div className="summary-row"><span>Subtotal</span><strong>{money(subtotal)}</strong></div><div className="summary-row"><span>Envio GLS</span><strong>{!lines.length ? money(0) : shipping ? money(shipping) : "Grátis"}</strong></div><div className="summary-row"><span>IVA</span><span>Incluído</span></div><div className="summary-row total"><span>Total</span><strong>{money(subtotal + shipping)}</strong></div>{lines.length ? <Link href="/checkout" className="btn red">Finalizar compra</Link> : null}<Link href="/catalogo" className="btn ghost">Continuar a comprar</Link></aside>
    </div></section>
  </>;
}
