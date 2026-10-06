import { NextResponse } from "next/server";
import { createSession, expectedLogin, sessionCookieName, sessionCookieOptions, type DemoRole } from "@/lib/server-session";

export async function POST(request:Request) {
  const body = await request.json().catch(()=>null) as {role?:DemoRole;username?:string;password?:string}|null;
  if (!body || !["customer","admin"].includes(body.role || "")) return NextResponse.json({detail:"Pedido inválido"},{status:400});
  const expected = expectedLogin(body.role as DemoRole);
  if (!expected.username || body.username !== expected.username || body.password !== expected.password) return NextResponse.json({detail:"Credenciais inválidas"},{status:401});
  const response = NextResponse.json({role:body.role, username:body.username});
  response.cookies.set(
    sessionCookieName,
    createSession(body.role as DemoRole, body.username || ""),
    sessionCookieOptions(),
  );
  return response;
}
