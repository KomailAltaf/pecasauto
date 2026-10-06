"use client";
import Link from "next/link";
import { ShoppingCart } from "lucide-react";
import { Product } from "@/lib/types";
import { useCart } from "./CartProvider";
import { FitmentBadge } from "./FitmentBadge";
import { PartVisual } from "./PartVisual";

export function ProductCard({product}:{product:Product}){const {add}=useCart();return <article className="product-card"><Link href={`/produto/${product.id}`}><PartVisual kind={product.image_kind}/></Link><div className="product-card-body"><span className="brand-label">{product.brand}</span><Link href={`/produto/${product.id}`}><h3>{product.name}</h3></Link><span className="reference">REF. {product.manufacturer_reference}</span><div style={{marginTop:14}}><FitmentBadge state={product.fitment_state}/></div><div className="product-meta"><div className="price">{product.price.toFixed(2).replace(".",",")} €<small>IVA incluído</small></div><div className={product.stock?"stock":"stock out"}>{product.stock?`${product.stock} em stock`:"Por encomenda"}<br/>{product.delivery_estimate}</div></div><div className="product-actions"><Link href={`/produto/${product.id}`} className="btn ghost small">Detalhes</Link><button className="btn small" onClick={()=>add(product)}><ShoppingCart size={16}/> Adicionar</button></div></div></article>}
