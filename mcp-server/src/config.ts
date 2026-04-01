import { PhoneClientConfig } from "./types.js";

function requireEnv(name: string): string {
  const val = process.env[name];
  if (!val) throw new Error(`Required env var ${name} is not set`);
  return val;
}

export function loadConfig(): PhoneClientConfig {
  return {
    phoneIp: requireEnv("PHONE_IP"),
    phonePort: parseInt(process.env["PHONE_PORT"] ?? "8080", 10),
    agentKey: requireEnv("PHONE_AGENT_KEY"),
    timeoutMs: parseInt(process.env["PHONE_TIMEOUT_MS"] ?? "60000", 10),
  };
}
