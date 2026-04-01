import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { PhoneClient } from "../client.js";

export function registerInfoTools(server: McpServer, client: PhoneClient): void {
  server.tool(
    "phone_info",
    "Get device information: battery status, WiFi connection, disk usage, and OS info.",
    {},
    async () => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.info(), null, 2) }] };
    }
  );
}
