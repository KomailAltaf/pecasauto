import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";
import { CartProvider } from "@/components/CartProvider";

export const metadata:Metadata={title:"PeçasAuto — Peças certas para o seu carro",description:"Protótipo de ecommerce automóvel português"};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="pt"><body><CartProvider><Header/><main>{children}</main><footer><div className="brand footer-brand">PEÇAS<span>AUTO</span></div><p>Protótipo local · dados e checkout demonstrativos</p><div><a href="/architecture">Arquitetura</a><a href="/admin/providers">Integrações</a></div></footer></CartProvider></body></html>}
