#!/usr/bin/env bash
set -e

echo "=== phone-mcp agent installer ==="
echo ""

if [ -z "$PREFIX" ] || [ ! -d "$PREFIX/bin" ]; then
  echo "ERROR: This script must be run inside Termux on Android."
  exit 1
fi

echo "[1/6] Updating Termux packages..."
pkg update -y -q

echo "[2/6] Installing Python, termux-api..."
pkg install -y -q python termux-api

echo "[3/6] Installing Python packages..."
pip install --quiet fastapi "uvicorn[standard]" pydantic pydantic-settings python-multipart

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  echo "[4/6] Generating API key..."
  API_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
  echo "PHONE_AGENT_KEY=$API_KEY" > "$ENV_FILE"
  echo "PHONE_AGENT_PORT=8080" >> "$ENV_FILE"
  echo "LOG_LEVEL=INFO" >> "$ENV_FILE"
  echo "Generated API key: $API_KEY"
else
  echo "[4/6] .env already exists, skipping."
  API_KEY=$(grep PHONE_AGENT_KEY "$ENV_FILE" | cut -d= -f2)
fi

echo "[5/6] Detecting Tailscale IP..."
TAILSCALE_IP=$(ip addr show tailscale0 2>/dev/null | grep 'inet ' | awk '{print $2}' | cut -d/ -f1 || echo "")
if [ -z "$TAILSCALE_IP" ]; then
  TAILSCALE_IP=$(tailscale ip -4 2>/dev/null || echo "NOT FOUND — install Tailscale first")
fi

echo "[6/6] Acquiring Termux wake-lock..."
termux-wake-lock 2>/dev/null || echo "  (wake-lock unavailable)"

echo ""
echo "======================================"
echo "  phone-mcp agent installed!"
echo "======================================"
echo ""
echo "  Tailscale IP : ${TAILSCALE_IP}"
echo "  Port         : 8080"
echo "  API Key      : ${API_KEY}"
echo ""
echo "  Start the agent:"
echo "    cd $SCRIPT_DIR && uvicorn phone_agent.main:app --host 0.0.0.0 --port 8080"
echo ""
echo "  Claude Code MCP config (~/.claude/mcp.json):"
echo '  { "mcpServers": { "phone": { "command": "node",'
echo '    "args": ["/path/to/phone-mcp/mcp-server/dist/index.js"],'
echo "    \"env\": { \"PHONE_IP\": \"${TAILSCALE_IP}\", \"PHONE_PORT\": \"8080\", \"PHONE_AGENT_KEY\": \"${API_KEY}\" } } } }"
echo ""
echo "  Required Android permissions: SMS, Contacts, Location, Camera, Storage"
echo "  Run: termux-setup-storage"
