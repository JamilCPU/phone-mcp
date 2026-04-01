import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerLocationTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_location", "Get the phone's GPS location. Requires Location permission.",
    {
      provider: z.enum(["gps", "network", "passive"]).default("gps")
        .describe("gps = accurate/slow, network = fast/less accurate"),
    },
    async ({ provider }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.location(provider), null, 2) }] };
    }
  );
}
