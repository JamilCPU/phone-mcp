import { PhoneClientConfig } from "./types.js";

export class PhoneClient {
  private baseUrl: string;
  private headers: Record<string, string>;
  private timeoutMs: number;
  private lastHealthCheck = 0;
  private lastHealthOk = false;

  constructor(config: PhoneClientConfig) {
    this.baseUrl = `http://${config.phoneIp}:${config.phonePort}`;
    this.headers = {
      "Authorization": `Bearer ${config.agentKey}`,
      "Content-Type": "application/json",
    };
    this.timeoutMs = config.timeoutMs;
  }

  private async request<T>(
    method: string,
    path: string,
    body?: unknown,
    params?: Record<string, string>,
    timeoutOverride?: number,
  ): Promise<T> {
    let url = `${this.baseUrl}${path}`;
    if (params && Object.keys(params).length > 0) {
      url += "?" + new URLSearchParams(params).toString();
    }
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), timeoutOverride ?? this.timeoutMs);
    try {
      const resp = await fetch(url, {
        method,
        headers: this.headers,
        body: body !== undefined ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });
      if (!resp.ok) {
        const text = await resp.text().catch(() => "");
        let detail = text;
        try { detail = JSON.parse(text)?.detail ?? text; } catch {}
        throw new Error(`Phone agent error ${resp.status}: ${detail}`);
      }
      return resp.json() as Promise<T>;
    } catch (err: unknown) {
      if (err instanceof Error && err.name === "AbortError") {
        throw new Error(`Phone agent at ${this.baseUrl} timed out. Is the agent running?`);
      }
      throw err;
    } finally {
      clearTimeout(timeout);
    }
  }

  async checkHealth(): Promise<boolean> {
    const now = Date.now();
    if (now - this.lastHealthCheck < 60_000 && this.lastHealthOk) return true;
    try {
      await this.request<{ status: string }>("GET", "/health", undefined, undefined, 5000);
      this.lastHealthOk = true;
    } catch {
      this.lastHealthOk = false;
      throw new Error(
        `Phone agent not responding at ${this.baseUrl}. ` +
        `Ensure: 1) Termux is running, 2) phone-agent is started, 3) Tailscale is connected.`
      );
    } finally {
      this.lastHealthCheck = now;
    }
    return true;
  }

  async shell(command: string, timeout = 30): Promise<unknown> {
    return this.request("POST", "/shell", { command, timeout }, undefined, (timeout + 5) * 1000);
  }
  async fileRead(path: string): Promise<unknown> { return this.request("GET", "/files", undefined, { path }); }
  async fileWrite(path: string, content: string, encoding = "utf-8"): Promise<unknown> {
    return this.request("POST", "/files", { path, content, encoding });
  }
  async fileList(path: string): Promise<unknown> { return this.request("GET", "/files/list", undefined, { path }); }
  async screenshot(): Promise<unknown> { return this.request("GET", "/screenshot", undefined, undefined, 30000); }
  async info(): Promise<unknown> { return this.request("GET", "/info"); }
  async notify(title: string, content: string, id = 1): Promise<unknown> {
    return this.request("POST", "/notification", { title, content, id });
  }
  async clipboardGet(): Promise<unknown> { return this.request("GET", "/clipboard"); }
  async clipboardSet(text: string): Promise<unknown> { return this.request("POST", "/clipboard", { text }); }
  async smsList(limit = 10): Promise<unknown> { return this.request("GET", "/sms", undefined, { limit: String(limit) }); }
  async smsSend(number: string, body: string): Promise<unknown> {
    return this.request("POST", "/sms", { number, body }, undefined, 45000);
  }
  async contacts(): Promise<unknown> { return this.request("GET", "/contacts", undefined, undefined, 30000); }
  async location(provider: "gps" | "network" | "passive" = "gps"): Promise<unknown> {
    return this.request("GET", "/location", undefined, { provider }, 35000);
  }
  async mediaCamera(cameraId = 0): Promise<unknown> {
    return this.request("POST", "/media/camera", { camera_id: cameraId }, undefined, 20000);
  }
  async mediaTorch(on: boolean): Promise<unknown> { return this.request("POST", "/media/torch", { on }); }
  async mediaVibrate(durationMs = 500): Promise<unknown> {
    return this.request("POST", "/media/vibrate", { duration_ms: durationMs });
  }
  async mediaTts(text: string, language = "en"): Promise<unknown> {
    return this.request("POST", "/media/tts", { text, language }, undefined, 35000);
  }
  async volumeGet(): Promise<unknown> { return this.request("GET", "/volume"); }
  async volumeSet(stream: string, value: number): Promise<unknown> {
    return this.request("POST", "/volume", { stream, value });
  }
  async appsList(): Promise<unknown> { return this.request("GET", "/apps", undefined, undefined, 25000); }
  async appsLaunch(pkg: string, activity = ""): Promise<unknown> {
    return this.request("POST", "/apps/launch", { package: pkg, activity });
  }
  async inputTap(x: number, y: number): Promise<unknown> { return this.request("POST", "/input/tap", { x, y }); }
  async inputSwipe(x1: number, y1: number, x2: number, y2: number, durationMs = 300): Promise<unknown> {
    return this.request("POST", "/input/swipe", { x1, y1, x2, y2, duration_ms: durationMs });
  }
  async inputText(text: string): Promise<unknown> { return this.request("POST", "/input/text", { text }); }
  async inputKey(keycode: string): Promise<unknown> { return this.request("POST", "/input/key", { keycode }); }
}
