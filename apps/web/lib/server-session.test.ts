import { createHmac } from "node:crypto";
import { describe, expect, it } from "vitest";

import {
  assertSessionConfiguration,
  createSession,
  sessionCookieOptions,
  verifySession,
} from "./server-session";

const SECRET = "a".repeat(48);
const OTHER_SECRET = "b".repeat(48);
const NOW = Date.UTC(2026, 9, 6, 9, 0, 0);

function signedPayload(payload: Record<string, unknown>, secret: string) {
  const encoded = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const signature = createHmac("sha256", secret).update(encoded).digest("base64url");
  return `${encoded}.${signature}`;
}

describe("server sessions", () => {
  it("accepts a valid, unexpired, versioned session", () => {
    const token = createSession("admin", "demo-admin", { secret: SECRET, now: NOW });
    expect(verifySession(token, { secret: SECRET, now: NOW + 1_000 })).toEqual({
      role: "admin",
      username: "demo-admin",
    });
  });

  it("prevents startup when SESSION_SECRET is missing or weak", () => {
    expect(() => assertSessionConfiguration({})).toThrow(/SESSION_SECRET is required/);
    expect(() => assertSessionConfiguration({ SESSION_SECRET: "short" })).toThrow(/at least 32 bytes/);
    const formerPublicSecret = ["local", "development", "session", "secret", "change", "me"].join("-");
    expect(() => assertSessionConfiguration({ SESSION_SECRET: formerPublicSecret })).toThrow(/public or predictable/);
  });

  it("rejects a session signed with the wrong secret", () => {
    const token = createSession("customer", "demo-customer", { secret: SECRET, now: NOW });
    expect(verifySession(token, { secret: OTHER_SECRET, now: NOW })).toBeNull();
  });

  it("rejects a cookie forged with the former public development secret", () => {
    const formerPublicSecret = ["local", "development", "session", "secret", "change", "me"].join("-");
    const token = signedPayload(
      { v: 1, role: "admin", username: "forged", iat: NOW / 1000, exp: NOW / 1000 + 28_800 },
      formerPublicSecret,
    );
    expect(verifySession(token, { secret: SECRET, now: NOW })).toBeNull();
  });

  it("rejects expired sessions", () => {
    const token = createSession("customer", "demo-customer", { secret: SECRET, now: NOW });
    expect(verifySession(token, { secret: SECRET, now: NOW + 28_800_000 })).toBeNull();
  });

  it("rejects a tampered payload", () => {
    const token = createSession("customer", "demo-customer", { secret: SECRET, now: NOW });
    const [payload, signature] = token.split(".");
    const parsed = JSON.parse(Buffer.from(payload, "base64url").toString("utf8"));
    parsed.role = "admin";
    const tampered = `${Buffer.from(JSON.stringify(parsed)).toString("base64url")}.${signature}`;
    expect(verifySession(tampered, { secret: SECRET, now: NOW })).toBeNull();
  });

  it("rejects a missing cookie and an unexpected schema version", () => {
    expect(verifySession(undefined, { secret: SECRET, now: NOW })).toBeNull();
    const token = signedPayload(
      { v: 2, role: "admin", username: "demo-admin", iat: NOW / 1000, exp: NOW / 1000 + 28_800 },
      SECRET,
    );
    expect(verifySession(token, { secret: SECRET, now: NOW })).toBeNull();
  });

  it("sets Secure only in production and always protects the cookie", () => {
    expect(sessionCookieOptions("production")).toMatchObject({
      httpOnly: true,
      sameSite: "lax",
      secure: true,
      maxAge: 28_800,
    });
    expect(sessionCookieOptions("development").secure).toBe(false);
  });
});
