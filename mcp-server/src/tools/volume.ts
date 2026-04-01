import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerVolumeTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_volume_get", "Get current volume levels for all audio streams.", {},
    async () => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.volumeGet(), null, 2) }] };
    }
  );
  server.tool("phone_volume_set", "Set volume for an audio stream (0-15).",
    {
      stream: z.enum(["music", "call", "ring", "alarm", "notification", "system"]),
      value: z.number().int().min(0).max(15),
    },
    async ({ stream, value }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.volumeSet(stream, value), null, 2) }] };
    }
  );
}
