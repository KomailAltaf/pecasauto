"use client";
import Link from "next/link";
import { CarFront, Menu, Search, ShoppingBag, UserRound, Wrench, X } from "lucide-react";
import { useState } from "react";
import { useCart } from "./CartProvider";

export function Header(){
  const [open,setOpen]=useState(false); const {count}=useCart();
  return <>
    <div className="utility"><span>ENTREGA EM PORTUGAL CONTINENTAL</span><span>APOIO EM PORTUGUÊS</span><span>PROTÓTIPO TÉCNICO</span></div>
    <header className="header">
      <Link href="/" className="brand" aria-label="PeçasAuto início"><span className="brand-mark"><Wrench size={22}/></span><span>PEÇAS<span>AUTO</span></span></Link>
      <nav className={open?"nav open":"nav"}>
        <Link href="/catalogo">Catálogo</Link><Link href="/garagem"><CarFront size={18}/> Meu Carro</Link><Link href="/architecture">Arquitetura</Link><Link href="/admin">Admin</Link>
      </nav>
      <div className="header-actions"><Link href="/catalogo" aria-label="Pesquisar"><Search/></Link><Link href="/login" className="icon-btn" aria-label="Entrar"><UserRound/></Link><Link href="/carrinho" className="cart-link"><ShoppingBag/><span>{count}</span></Link><button className="menu-btn" onClick={()=>setOpen(!open)} aria-label="Menu">{open?<X/>:<Menu/>}</button></div>
    </header>
  </>
}
