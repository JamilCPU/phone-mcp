# Termux Setup Guide

## Step 1: Install Termux from F-Droid

> **Do NOT use the Play Store version** — it is outdated. Install [Termux](https://f-droid.org/en/packages/com.termux/) and [Termux:API](https://f-droid.org/en/packages/com.termux.api/) from **F-Droid**.

## Step 2: Install dependencies

```bash
pkg update && pkg upgrade -y
pkg install python termux-api git
```

## Step 3: Grant Android permissions

Settings > Apps > Termux > Permissions:

| Permission | Required for |
|-----------|-------------|
| Storage | phone_file_* |
| SMS | phone_sms_* |
| Contacts | phone_contacts_list |
| Location | phone_location |
| Camera | phone_camera |

Then run: `termux-setup-storage`

## Step 4: Install Tailscale

Install from Play Store, sign in, enable VPN, then:

```bash
tailscale ip -4
```

## Step 5: Clone and install

```bash
git clone https://github.com/JamilCPU/phone-mcp
cd phone-mcp/phone-agent
bash install.sh
```

The installer generates your API key and detects Tailscale IP.

## Step 6: Start the agent

```bash
uvicorn phone_agent.main:app --host 0.0.0.0 --port 8080
```

## Step 7: Keep alive with wake-lock

```bash
termux-wake-lock
```

Add alias to ~/.bashrc:
```bash
alias start-agent='cd ~/phone-mcp/phone-agent && termux-wake-lock && uvicorn phone_agent.main:app --host 0.0.0.0 --port 8080'
```

## Step 8: Enable Accessibility Service (screenshots)

Settings > Accessibility > Installed Services > Termux:API > Enable

## Permissions Reference

| Tool | Android Permission |
|------|------------------|
| phone_shell | None |
| phone_file_* | Storage |
| phone_screenshot | Accessibility service |
| phone_notification | Notifications |
| phone_sms_* | SMS |
| phone_contacts_list | Contacts |
| phone_location | Location |
| phone_camera | Camera |

## Troubleshooting

**termux-camera-photo not found**: `pkg install termux-api` + install Termux:API app from F-Droid

**Permission denied (SMS/Contacts)**: Settings > Apps > Termux > Permissions

**Screenshot fails**: Enable Termux:API accessibility service

**Agent stops when screen off**: Run `termux-wake-lock` before starting

**Tailscale IP not found**: Open Tailscale app, check "This device"
