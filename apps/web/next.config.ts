import type { NextConfig } from "next";
import { assertSessionConfiguration } from "./lib/server-session";

assertSessionConfiguration();

const nextConfig: NextConfig = {
  reactStrictMode: true,
  outputFileTracingRoot: process.cwd(),
};

export default nextConfig;
