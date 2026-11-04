# phone-mcp

> Control your Android phone with AI models over Tailscale

**phone-mcp** lets Claude (or any MCP-compatible AI) control your Android phone. A lightweight HTTP agent runs in [Termux](https://termux.dev) on your phone; an MCP server runs on your PC — connected securely over [Tailscale](https://tailscale.com).

## What can the AI do?

| Category | Capabilities |
|----------|-------------|
| **Shell** | Run any shell command |
| **Files** | Read, write, list files |
| **Screen** | Take screenshots |
| **Notifications** | Send push notifications |
| **Messaging** | Read and send SMS |
| **Contacts** | List contacts |
| **Location** | GPS coordinates |
| **Camera** | Take photos |
| **Media** | Flashlight, vibrate, text-to-speech |
| **Volume** | Get/set volume for any stream |
| **Apps** | List and launch apps |
| **UI Automation** | Tap, swipe, type, press keys |

## Architecture

```
Claude Code <-- MCP (stdio) --> mcp-server (PC)
                                      |
                                 HTTP / Tailscale
                                      |
                               phone-agent (Termux)
                                      |
                               Android APIs + Shell
```

**Security**: Traffic goes over Tailscale (WireGuard). Every request requires a shared API key. The phone is never exposed to the public internet.

## Stack

- Phone agent: Python 3.10+, FastAPI served by uvicorn, Termux and Termux:API, tested with pytest and linted with ruff
- MCP server: TypeScript on Node.js 18+, `@modelcontextprotocol/sdk`, zod, tested with vitest
- Tailscale (WireGuard) for the private connection; GitHub Actions CI

## Running

### 1. Phone (Termux)

Install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:API](https://f-droid.org/en/packages/com.termux.api/) from **F-Droid** (not Play Store).

```bash
pkg install git python termux-api
git clone https://github.com/JamilCPU/phone-mcp
cd phone-mcp/phone-agent
bash install.sh
uvicorn phone_agent.main:app --host 0.0.0.0 --port 8080
```

`install.sh` prints your Tailscale IP and API key — save both.

### 2. PC

```bash
cd phone-mcp/mcp-server
npm install && npm run build
```

### 3. Claude Code

Add to `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "phone": {
      "command": "node",
      "args": ["/path/to/phone-mcp/mcp-server/dist/index.js"],
      "env": {
        "PHONE_IP": "<phone-tailscale-ip>",
        "PHONE_PORT": "8080",
        "PHONE_AGENT_KEY": "your-key-from-install-sh"
      }
    }
  }
}
```

Restart Claude Code — you now have 25+ phone tools available.

## Example Prompts

```
"Take a screenshot of my phone and describe what's on screen"
"Send a notification: Build complete"
"What's my battery level and WiFi network?"
"Open Spotify on my phone"
"What's my current GPS location?"
"List files in /sdcard/Download"
"Make my phone say hello"
"Send an SMS to <phone-number>: I'll be 10 minutes late"
```

See [docs/examples.md](docs/examples.md) for 35+ examples.

## Requirements

- Android phone with Termux + Termux:API (from F-Droid)
- Tailscale on both phone and PC
- Node.js 18+ on PC
- Python 3.10+ in Termux

## Docs

- [Termux Setup](docs/setup-termux.md)
- [Tailscale Setup](docs/setup-tailscale.md)
- [Tool Reference](docs/tool-reference.md)
- [Examples](docs/examples.md)

## License

MIT
