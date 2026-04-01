# Tailscale Setup Guide

Tailscale creates a private WireGuard network between your devices.

## Step 1: Install on Android

Install [Tailscale](https://play.google.com/store/apps/details?id=com.tailscale.ipn.android) from Play Store.

## Step 2: Sign in and enable VPN

Open Tailscale, sign in, tap the toggle to enable.

## Step 3: Find your phone IP

In the Tailscale app: tap "This device".
Or in Termux:

```bash
tailscale ip -4
```

## Step 4: Set up on your PC

Install Tailscale on your PC and sign in with the **same account**.

## Step 5: Verify connectivity

```bash
ping 100.x.x.x
```

## Magic DNS (optional)

Use your phone hostname instead of raw IP:
`<device-name>.<tailnet>.ts.net`

Find it at login.tailscale.com/admin/machines.

## Security

- Phone-agent only listens on the Tailscale interface
- All traffic is WireGuard-encrypted
- API key provides additional authentication
- Phone is never reachable from the public internet
