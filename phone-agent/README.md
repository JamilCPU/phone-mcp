# phone-agent

HTTP server that runs inside **Termux on Android** and exposes phone capabilities as REST endpoints.

## Quick Install (Termux)

```bash
pkg install git
git clone https://github.com/JamilCPU/phone-mcp
cd phone-mcp/phone-agent
bash install.sh
uvicorn phone_agent.main:app --host 0.0.0.0 --port 8080
```

## API Docs

Visit `http://<phone-ip>:8080/docs` for the interactive Swagger UI.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /health | Health check (no auth required) |
| POST | /shell | Execute shell command |
| GET | /files | Read file |
| POST | /files | Write file |
| GET | /files/list | List directory |
| GET | /info | Device info |
| GET | /screenshot | Capture screen |
| POST | /notification | Send notification |
| GET | /clipboard | Read clipboard |
| POST | /clipboard | Set clipboard |
| GET | /sms | List SMS |
| POST | /sms | Send SMS |
| GET | /contacts | List contacts |
| GET | /location | GPS location |
| POST | /media/camera | Take photo |
| POST | /media/torch | Toggle flashlight |
| POST | /media/vibrate | Vibrate |
| POST | /media/tts | Text-to-speech |
| GET | /volume | Get volume |
| POST | /volume | Set volume |
| GET | /apps | List apps |
| POST | /apps/launch | Launch app |
| POST | /input/tap | Tap coordinates |
| POST | /input/swipe | Swipe gesture |
| POST | /input/text | Type text |
| POST | /input/key | Press key |

## Authentication

Set `PHONE_AGENT_KEY` in `.env`. All endpoints except `/health` require `Authorization: Bearer <key>`.
