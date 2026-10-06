import { NextRequest, NextResponse } from "next/server";
import { sessionCookieName, verifySession, type DemoRole } from "@/lib/server-session";

const API = process.env.FASTAPI_API_URL || "http://127.0.0.1:8000";
const requiredRole = (path:string[]):DemoRole => path[0] === "admin" || path[0] === "providers" ? "admin" : "customer";
const apiCredential = (role:DemoRole) => role === "admin" ? process.env.FASTAPI_ADMIN_AUTH : process.env.FASTAPI_CUSTOMER_AUTH;

async function proxy(request:NextRequest, context:{params:Promise<{path:string[]}>}) {
  const {path} = await context.params;
  const role = requiredRole(path);
  const session = verifySession(request.cookies.get(sessionCookieName)?.value);
  if (!session || session.role !== role) return NextResponse.json({detail:`Sessão ${role} necessária`},{status:401});
  const credential = apiCredential(role);
  if (!credential) return NextResponse.json({detail:"Credencial interna FastAPI não configurada"},{status:503});
  const target = new URL(`/api/${path.join("/")}`, API);
  target.search = request.nextUrl.search;
  const body = ["GET","HEAD"].includes(request.method) ? undefined : await request.arrayBuffer();
  const upstream = await fetch(target, {method:request.method, body, cache:"no-store", headers:{"Content-Type":request.headers.get("content-type")||"application/json",Authorization:`Basic ${Buffer.from(credential).toString("base64")}`}});
  return new NextResponse(upstream.body,{status:upstream.status,headers:{"Content-Type":upstream.headers.get("content-type")||"application/json"}});
}
export const GET=proxy; export const POST=proxy; export const DELETE=proxy; export const PUT=proxy; export const PATCH=proxy;
