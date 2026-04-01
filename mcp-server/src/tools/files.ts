import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerFileTools(server: McpServer, client: PhoneClient): void {
  server.tool(
    "phone_file_read",
    "Read a file from the phone. Returns UTF-8 text or base64 for binary files.",
    { path: z.string().describe("Absolute file path, e.g. /sdcard/Download/file.txt") },
    async ({ path }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.fileRead(path), null, 2) }] };
    }
  );

  server.tool(
    "phone_file_write",
    "Write content to a file on the phone. Creates parent directories if needed.",
    {
      path: z.string().describe("Absolute file path on the phone"),
      content: z.string().describe("File content"),
      encoding: z.enum(["utf-8", "base64"]).default("utf-8"),
    },
    async ({ path, content, encoding }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.fileWrite(path, content, encoding), null, 2) }] };
    }
  );

  server.tool(
    "phone_file_list",
    "List files and directories at a path on the phone.",
    { path: z.string().default("/sdcard").describe("Absolute directory path") },
    async ({ path }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.fileList(path), null, 2) }] };
    }
  );
}
