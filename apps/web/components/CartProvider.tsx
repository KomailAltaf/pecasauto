"use client";
import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from "react";
import { addLine, cartSubtotal } from "@/lib/cart";
import { CartLine, Product } from "@/lib/types";

type CartContextValue={lines:CartLine[];add:(p:Product)=>void;remove:(id:number)=>void;setQuantity:(id:number,q:number)=>void;clear:()=>void;count:number;subtotal:number};
const CartContext=createContext<CartContextValue|null>(null);
export function CartProvider({children}:{children:ReactNode}){
  const [lines,setLines]=useState<CartLine[]>([]);
  useEffect(()=>{try{setLines(JSON.parse(localStorage.getItem("pecasauto-cart")||"[]"))}catch{}},[]);
  useEffect(()=>{localStorage.setItem("pecasauto-cart",JSON.stringify(lines))},[lines]);
  const value=useMemo(()=>({lines,add:(p:Product)=>setLines(v=>addLine(v,p)),remove:(id:number)=>setLines(v=>v.filter(x=>x.product.id!==id)),setQuantity:(id:number,q:number)=>setLines(v=>v.map(x=>x.product.id===id?{...x,quantity:Math.max(1,q)}:x)),clear:()=>setLines([]),count:lines.reduce((n,l)=>n+l.quantity,0),subtotal:cartSubtotal(lines)}),[lines]);
  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}
export const useCart=()=>{const value=useContext(CartContext);if(!value)throw new Error("CartProvider missing");return value};
