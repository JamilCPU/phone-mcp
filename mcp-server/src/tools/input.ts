import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerInputTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_tap", "Tap at screen coordinates. Use phone_screenshot first to find coordinates.",
    {
      x: z.number().int().min(0).describe("X coordinate in pixels"),
      y: z.number().int().min(0).describe("Y coordinate in pixels"),
    },
    async ({ x, y }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.inputTap(x, y), null, 2) }] };
    }
  );
  server.tool("phone_swipe", "Swipe on the phone screen.",
    {
      x1: z.number().int().min(0), y1: z.number().int().min(0),
      x2: z.number().int().min(0), y2: z.number().int().min(0),
      duration_ms: z.number().int().min(50).max(5000).default(300),
    },
    async ({ x1, y1, x2, y2, duration_ms }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.inputSwipe(x1, y1, x2, y2, duration_ms), null, 2) }] };
    }
  );
  server.tool("phone_type", "Type text into the focused input field.",
    { text: z.string().min(1) },
    async ({ text }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.inputText(text), null, 2) }] };
    }
  );
  server.tool("phone_key", "Press an Android key event. Common: KEYCODE_BACK, KEYCODE_HOME, KEYCODE_ENTER.",
    { keycode: z.string().describe("Keycode name or number") },
    async ({ keycode }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.inputKey(keycode), null, 2) }] };
    }
  );
}
