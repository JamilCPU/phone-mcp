import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerSmsTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_sms_list", "List recent SMS messages. Requires SMS permission.",
    { limit: z.number().int().min(1).max(100).default(10) },
    async ({ limit }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.smsList(limit), null, 2) }] };
    }
  );
  server.tool("phone_sms_send", "Send an SMS message. WARNING: sends a real SMS.",
    {
      number: z.string().min(1).describe("Phone number"),
      body: z.string().min(1).describe("Message body"),
    },
    async ({ number, body }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.smsSend(number, body), null, 2) }] };
    }
  );
}
