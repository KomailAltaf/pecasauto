import { createHash, createHmac, timingSafeEqual } from "node:crypto";

export type DemoRole = "customer" | "admin";

type SessionPayload = {
  v: 1;
  role: DemoRole;
  username: string;
  iat: number;
  exp: number;
};

type SessionOptions = {
  secret?: string;
  now?: number;
};

const COOKIE = "pecasauto_demo_session";
const SESSION_VERSION = 1;
const SESSION_TTL_SECONDS = 60 * 60 * 8;
const MINIMUM_SECRET_BYTES = 32;
const FORBIDDEN_SECRET_FINGERPRINTS = new Set([
  "b0343665c1e60189bcba5028af12b186fa9bc0a4478ed24cb13f20d8c669e505",
]);

function validateSecret(value: string | undefined): string {
  if (!value) {
    throw new Error("SESSION_SECRET is required. Generate one with: openssl rand -base64 48");
  }
  if (Buffer.byteLength(value, "utf8") < MINIMUM_SECRET_BYTES) {
    throw new Error("SESSION_SECRET must contain at least 32 bytes of strong random data");
  }
  const fingerprint = createHash("sha256").update(value).digest("hex");
  if (
    FORBIDDEN_SECRET_FINGERPRINTS.has(fingerprint) ||
    /^(default|example|password|secret|change[-_ ]?me)([-_ ].*)?$/i.test(value)
  ) {
    throw new Error("SESSION_SECRET must not use a public or predictable placeholder");
  }
  return value;
}

function configuredSecret(override?: string): string {
  return validateSecret(override ?? process.env.SESSION_SECRET);
}

function sign(value: string, sessionSecret: string): string {
  return createHmac("sha256", sessionSecret).update(value).digest("base64url");
}

export function assertSessionConfiguration(env: NodeJS.ProcessEnv = process.env): void {
  validateSecret(env.SESSION_SECRET);
}

export function createSession(role: DemoRole, username: string, options: SessionOptions = {}): string {
  const sessionSecret = configuredSecret(options.secret);
  const issuedAt = Math.floor((options.now ?? Date.now()) / 1000);
  const body: SessionPayload = {
    v: SESSION_VERSION,
    role,
    username,
    iat: issuedAt,
    exp: issuedAt + SESSION_TTL_SECONDS,
  };
  const payload = Buffer.from(JSON.stringify(body)).toString("base64url");
  return `${payload}.${sign(payload, sessionSecret)}`;
}

export function verifySession(
  token: string | undefined,
  options: SessionOptions = {},
): { role: DemoRole; username: string } | null {
  if (!token) return null;
  const sessionSecret = configuredSecret(options.secret);
  const parts = token.split(".");
  if (parts.length !== 2) return null;
  const [payload, signature] = parts;
  if (!payload || !signature) return null;

  const expected = sign(payload, sessionSecret);
  const receivedBuffer = Buffer.from(signature);
  const expectedBuffer = Buffer.from(expected);
  if (
    receivedBuffer.length !== expectedBuffer.length ||
    !timingSafeEqual(receivedBuffer, expectedBuffer)
  ) return null;

  try {
    const parsed = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")) as Partial<SessionPayload>;
    const now = Math.floor((options.now ?? Date.now()) / 1000);
    const validRole = parsed.role === "customer" || parsed.role === "admin";
    const validTimes =
      Number.isInteger(parsed.iat) &&
      Number.isInteger(parsed.exp) &&
      (parsed.exp as number) > (parsed.iat as number) &&
      (parsed.exp as number) - (parsed.iat as number) === SESSION_TTL_SECONDS &&
      now >= (parsed.iat as number) &&
      now < (parsed.exp as number);

    if (
      parsed.v !== SESSION_VERSION ||
      !validRole ||
      typeof parsed.username !== "string" ||
      parsed.username.length === 0 ||
      !validTimes
    ) return null;

    return { role: parsed.role as DemoRole, username: parsed.username };
  } catch {
    return null;
  }
}

export function sessionCookieOptions(environment = process.env.NODE_ENV) {
  return {
    httpOnly: true as const,
    sameSite: "lax" as const,
    secure: environment === "production",
    path: "/",
    maxAge: SESSION_TTL_SECONDS,
  };
}

export const sessionCookieName = COOKIE;
export const sessionTtlSeconds = SESSION_TTL_SECONDS;

export function expectedLogin(role: DemoRole) {
  const pair = role === "admin" ? process.env.DEMO_ADMIN_LOGIN : process.env.DEMO_CUSTOMER_LOGIN;
  const [username, ...passwordParts] = (pair || "").split(":");
  return { username, password: passwordParts.join(":") };
}
