import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { PhoneClient } from "../client.js";

export function registerContactsTools(server: McpServer, client: PhoneClient): void {
  server.tool("phone_contacts_list", "List contacts from the phone. Requires Contacts permission.", {},
    async () => {
      await client.checkHealth();
      return { content: [{ type: "text", text: JSON.stringify(await client.contacts(), null, 2) }] };
    }
  );
}
