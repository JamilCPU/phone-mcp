import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerShellTools(server: McpServer, client: PhoneClient): void {
  server.tool(
    "phone_shell",
    "Execute a shell command on the phone via Termux. Returns stdout, stderr, exit_code. WARNING: Commands run directly on the device. Dangerous commands are blocked.",
    {
      command: z.string().min(1).describe("Shell command to run on the phone"),
      timeout: z.number().int().min(1).max(300).default(30).describe("Timeout in seconds"),
    },
    async ({ command, timeout }) => {
      await client.checkHealth();
      const result = await client.shell(command, timeout);
      return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
    }
  );
}
