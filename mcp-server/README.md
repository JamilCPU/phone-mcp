# phone-mcp server

TypeScript MCP server bridging Claude Code to the phone-agent on your Android phone.

## Setup

```bash
npm install && npm run build
```

## Claude Code config (~/.claude/mcp.json)

```json
{
  "mcpServers": {
    "phone": {
      "command": "node",
      "args": ["/path/to/phone-mcp/mcp-server/dist/index.js"],
      "env": {
        "PHONE_IP": "<phone-tailscale-ip>",
        "PHONE_PORT": "8080",
        "PHONE_AGENT_KEY": "your-key"
      }
    }
  }
}
```

## Tools

`phone_shell`, `phone_file_read/write/list`, `phone_info`, `phone_screenshot`,
`phone_notification`, `phone_clipboard_get/set`, `phone_sms_list/send`,
`phone_contacts_list`, `phone_location`, `phone_camera`, `phone_torch`,
`phone_vibrate`, `phone_tts`, `phone_volume_get/set`, `phone_app_list/launch`,
`phone_tap`, `phone_swipe`, `phone_type`, `phone_key`
