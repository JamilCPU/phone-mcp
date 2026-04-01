import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerMediaTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_camera", "Take a photo with the phone camera. Returns JPEG image.",
    { camera_id: z.number().int().min(0).max(3).default(0).describe("0=back, 1=front") },
    async ({ camera_id }) => {
      await client.checkHealth();
      const r = await client.mediaCamera(camera_id) as { image: string };
      return { content: [{ type: "image", data: r.image, mimeType: "image/jpeg" }] };
    }
  );
  server.tool("phone_torch", "Toggle the phone flashlight on or off.",
    { on: z.boolean().describe("true = on, false = off") },
    async ({ on }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.mediaTorch(on), null, 2) }] };
    }
  );
  server.tool("phone_vibrate", "Make the phone vibrate.",
    { duration_ms: z.number().int().min(100).max(10000).default(500) },
    async ({ duration_ms }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.mediaVibrate(duration_ms), null, 2) }] };
    }
  );
  server.tool("phone_tts", "Make the phone speak text aloud.",
    {
      text: z.string().min(1).describe("Text to speak"),
      language: z.string().default("en").describe("Language code, e.g. en, es, fr"),
    },
    async ({ text, language }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.mediaTts(text, language), null, 2) }] };
    }
  );
}
