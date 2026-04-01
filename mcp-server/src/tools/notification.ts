import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerNotificationTools(server: McpServer, client: PhoneClient): void {
  server.tool(
    "phone_notification",
    "Send a push notification to the phone's notification drawer.",
    {
      title: z.string().min(1).describe("Notification title"),
      content: z.string().default("").describe("Notification body"),
      id: z.number().int().default(1).describe("Notification ID (same ID replaces previous)"),
    },
    async ({ title, content, id }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.notify(title, content, id), null, 2) }] };
    }
  );
}
