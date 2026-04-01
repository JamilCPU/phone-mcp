import { describe, it, expect, vi } from "vitest";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { PhoneClient } from "../src/client.js";
import { registerAllTools } from "../src/tools/index.js";

function makeClient(): PhoneClient {
  const stub = vi.fn().mockResolvedValue({});
  return {
    checkHealth: stub, shell: stub, fileRead: stub, fileWrite: stub, fileList: stub,
    info: stub, screenshot: vi.fn().mockResolvedValue({ image: "abc", format: "png" }),
    notify: stub, clipboardGet: stub, clipboardSet: stub, smsList: stub, smsSend: stub,
    contacts: stub, location: stub,
    mediaCamera: vi.fn().mockResolvedValue({ image: "abc", format: "jpeg" }),
    mediaTorch: stub, mediaVibrate: stub, mediaTts: stub,
    volumeGet: stub, volumeSet: stub, appsList: stub, appsLaunch: stub,
    inputTap: stub, inputSwipe: stub, inputText: stub, inputKey: stub,
  } as unknown as PhoneClient;
}

describe("Tool registrations", () => {
  it("registers all tools without throwing", () => {
    const server = new McpServer({ name: "test", version: "0.0.1" });
    expect(() => registerAllTools(server, makeClient())).not.toThrow();
  });
});
