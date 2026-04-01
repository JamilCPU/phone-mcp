import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { PhoneClient } from "../client.js";
import { registerShellTools } from "./shell.js";
import { registerFileTools } from "./files.js";
import { registerInfoTools } from "./info.js";
import { registerScreenshotTools } from "./screenshot.js";
import { registerNotificationTools } from "./notification.js";
import { registerClipboardTools } from "./clipboard.js";
import { registerSmsTools } from "./sms.js";
import { registerContactsTools } from "./contacts.js";
import { registerLocationTools } from "./location.js";
import { registerMediaTools } from "./media.js";
import { registerVolumeTools } from "./volume.js";
import { registerAppsTools } from "./apps.js";
import { registerInputTools } from "./input.js";

export function registerAllTools(server: McpServer, client: PhoneClient): void {
  registerShellTools(server, client);
  registerFileTools(server, client);
  registerInfoTools(server, client);
  registerScreenshotTools(server, client);
  registerNotificationTools(server, client);
  registerClipboardTools(server, client);
  registerSmsTools(server, client);
  registerContactsTools(server, client);
  registerLocationTools(server, client);
  registerMediaTools(server, client);
  registerVolumeTools(server, client);
  registerAppsTools(server, client);
  registerInputTools(server, client);
}
