"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { MessageCircle, ShoppingCart, Truck } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { getProductEditorial } from "@/lib/cms";
import { Product, VehicleCandidate } from "@/lib/types";
import { FitmentBadge } from "@/components/FitmentBadge";
import { PartVisual } from "@/components/PartVisual";
import { useCart } from "@/components/CartProvider";

export default function ProductPage() {
  const { id } = useParams<{id:string}>();
  const [product, setProduct] = useState<Product | null>(null);
  const [vehicle, setVehicle] = useState<VehicleCandidate | null>(null);
  const [editorial, setEditorial] = useState<any>(null);
  const { add } = useCart();
  useEffect(() => {
    api.product(id).then(item => { setProduct(item); getProductEditorial(item.sku).then(setEditorial); });
    try { setVehicle(JSON.parse(localStorage.getItem("pecasauto-active-vehicle-v2") || "null")); } catch {}
  }, [id]);
  if (!product) return <section className="section"><div className="container">A carregar produto…</div></section>;
  return <>
    <section className="page-hero"><div className="container"><span className="eyebrow" style={{color:"#83d3ad"}}>{product.category}</span><h1>{editorial?.brand?.name || product.brand}</h1><p>Referência sintética {product.manufacturer_reference} · dados demonstrativos</p></div></section>
    <section className="section"><div className="container product-detail"><PartVisual kind={product.image_kind} large/><div className="product-info">
      <span className="brand-label">{editorial?.brand?.name || product.brand}</span>
      <h1>{editorial?.displayName || product.name}</h1>
      {editorial?.shortDescription && <p className="section-copy">{editorial.shortDescription}</p>}
      <p className="reference">REF. {product.manufacturer_reference} · SKU {product.sku}</p>
      <span className={`tag ${editorial ? "real-tested" : "demo"}`}>{editorial ? "STRAPI · PUBLISHED EDITORIAL" : "CMS EDITORIAL UNAVAILABLE"}</span>
      <div style={{margin:"20px 0"}}><FitmentBadge state={product.fitment_state}/></div>
      {vehicle ? <div className="vehicle-context"><div><strong>{vehicle.make} {vehicle.model} {vehicle.generation}</strong><span>{vehicle.engine} · {vehicle.power_kw} kW</span></div></div> : <div className="warning-box">Selecione o seu veículo para iniciar a verificação.</div>}
      <div className="warning-box"><strong>COMPATIBILIDADE POR VERIFICAR</strong><br/>Sem FitmentProvider licenciado, este produto nunca é apresentado como compatível ou incompatível.</div>
      <div className="buy-box"><div style={{display:"flex",justifyContent:"space-between",alignItems:"end"}}><div className="price">{product.price.toFixed(2).replace(".",",")} €<small>IVA incluído · DEMO</small></div><div className={product.stock ? "stock" : "stock out"}>{product.stock ? `${product.stock} em stock · DEMO` : "Por encomenda · DEMO"}<br/>{product.delivery_estimate}</div></div><button className="btn red" style={{width:"100%",marginTop:18}} onClick={() => add(product)}><ShoppingCart/> Adicionar ao carrinho</button></div>
      <table className="spec-table"><tbody><tr><td>Referências OE</td><td>{product.oe_references.join(" · ")}</td></tr><tr><td>EAN</td><td>{product.ean}</td></tr>{Object.entries(product.attributes).map(([key, value]) => <tr key={key}><td>{key}</td><td>{value}</td></tr>)}</tbody></table>
      <div className="product-actions"><button className="btn ghost"><MessageCircle size={17}/> Perguntar sobre compatibilidade</button><span className="btn ghost"><Truck size={17}/> {product.delivery_estimate}</span></div>
    </div></div></section>
    <section className="section" style={{background:"white"}}><div className="container"><span className="eyebrow">Alternativas</span><h2 className="section-title" style={{fontSize:38}}>Compare outras marcas.</h2><Link className="btn" href={`/catalogo?category=${encodeURIComponent(product.category)}`}>Ver alternativas</Link></div></section>
  </>;
}
