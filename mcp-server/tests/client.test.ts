import { describe, it, expect, vi, beforeEach } from "vitest";
import { PhoneClient } from "../src/client.js";

const config = { phoneIp: "100.0.0.1", phonePort: 8080, agentKey: "test-key", timeoutMs: 5000 };

describe("PhoneClient", () => {
  beforeEach(() => { vi.restoreAllMocks(); });

  it("includes Authorization header", async () => {
    const mockFetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ status: "ok" }) });
    vi.stubGlobal("fetch", mockFetch);
    const client = new PhoneClient(config);
    await client.checkHealth();
    const [, opts] = mockFetch.mock.calls[0] as [string, RequestInit];
    expect((opts.headers as Record<string, string>)["Authorization"]).toBe("Bearer test-key");
  });

  it("throws on non-ok response", async () => {
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({
      ok: false, status: 401, text: async () => JSON.stringify({ detail: "Invalid token" }),
    }));
    await expect(new PhoneClient(config).shell("echo hi")).rejects.toThrow("401");
  });

  it("throws helpful message on timeout", async () => {
    vi.stubGlobal("fetch", vi.fn().mockImplementation(() => new Promise((_, reject) => {
      const err = new Error("aborted"); err.name = "AbortError"; setTimeout(() => reject(err), 10);
    })));
    await expect(new PhoneClient({ ...config, timeoutMs: 1 }).checkHealth()).rejects.toThrow(/not responding|timed out/i);
  });

  it("caches health check within 60s", async () => {
    const mockFetch = vi.fn().mockResolvedValue({ ok: true, json: async () => ({ status: "ok" }) });
    vi.stubGlobal("fetch", mockFetch);
    const client = new PhoneClient(config);
    await client.checkHealth();
    await client.checkHealth();
    expect(mockFetch).toHaveBeenCalledTimes(1);
  });
});
