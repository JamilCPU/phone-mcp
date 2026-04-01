import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerClipboardTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_clipboard_get", "Read the current clipboard from the phone.", {},
    async () => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.clipboardGet(), null, 2) }] };
    }
  );
  server.tool("phone_clipboard_set", "Set the phone clipboard to the given text.",
    { text: z.string().describe("Text to copy to clipboard") },
    async ({ text }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.clipboardSet(text), null, 2) }] };
    }
  );
}
