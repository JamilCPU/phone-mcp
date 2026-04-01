#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { loadConfig } from "./config.js";
import { PhoneClient } from "./client.js";
import { registerAllTools } from "./tools/index.js";

async function main() {
  let config;
  try {
    config = loadConfig();
  } catch (err) {
    process.stderr.write(`[phone-mcp] Config error: ${(err as Error).message}\n`);
    process.exit(1);
  }

  const client = new PhoneClient(config);
  const server = new McpServer({ name: "phone-mcp", version: "0.1.0" });
  registerAllTools(server, client);

  const transport = new StdioServerTransport();
  await server.connect(transport);
  process.stderr.write(`[phone-mcp] Connected — phone at ${config.phoneIp}:${config.phonePort}\n`);
}

main().catch((err) => {
  process.stderr.write(`[phone-mcp] Fatal: ${err}\n`);
  process.exit(1);
});
