import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { PhoneClient } from "../client.js";

export function registerAppsTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_app_list", "List all third-party installed apps (package names).", {},
    async () => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.appsList(), null, 2) }] };
    }
  );
  server.tool("phone_app_launch", "Launch an app by package name.",
    {
      package: z.string().min(1).describe("Package name, e.g. com.android.chrome"),
      activity: z.string().default("").describe("Optional activity name"),
    },
    async ({ package: pkg, activity }) => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.appsLaunch(pkg, activity), null, 2) }] };
    }
  );
}
