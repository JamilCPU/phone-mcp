import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { PhoneClient } from "../client.js";

export function registerScreenshotTools(server: McpServer, client: PhoneClient): void {
  server.tool(
    "phone_screenshot",
    "Take a screenshot of the phone screen. Returns a PNG image. Requires termux-api accessibility service.",
    {},
    async () => {
      await client.checkHealth();
      const result = await client.screenshot() as { image: string; format: string };
      return { content: [{ type: "image", data: result.image, mimeType: "image/png" }] };
    }
  );
}
