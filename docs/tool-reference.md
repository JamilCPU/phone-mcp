# Tool Reference

All 25+ tools organized by category.

---

## Shell

### phone_shell
Run a shell command on the phone.

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| command | string | required | Shell command |
| timeout | int | 30 | Max seconds (300 max) |

Returns: `{ stdout, stderr, exit_code, blocked }`

---

## Files

### phone_file_read
| Param | Type | Description |
|-------|------|-------------|
| path | string | Absolute path, e.g. /sdcard/notes.txt |

### phone_file_write
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| path | string | required | Absolute path |
| content | string | required | Content |
| encoding | string | utf-8 | utf-8 or base64 |

### phone_file_list
| Param | Type | Default |
|-------|------|--------|
| path | string | /sdcard |

---

## Device Info

### phone_info
No parameters. Returns battery, wifi, disk, uname.

---

## Screen

### phone_screenshot
No parameters. Returns PNG image. Requires Termux:API accessibility service.

---

## Notifications

### phone_notification
| Param | Type | Default |
|-------|------|--------|
| title | string | required |
| content | string | "" |
| id | int | 1 |

---

## Clipboard

### phone_clipboard_get — No parameters
### phone_clipboard_set
| Param | Type |
|-------|------|
| text | string |

---

## Messaging

### phone_sms_list
| Param | Type | Default |
|-------|------|--------|
| limit | int | 10 (max 100) |

### phone_sms_send — WARNING: sends a real SMS
| Param | Type |
|-------|------|
| number | string |
| body | string |

---

## Contacts

### phone_contacts_list — No parameters. Requires Contacts permission.

---

## Location

### phone_location
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| provider | string | gps | gps/network/passive |

Returns: latitude, longitude, altitude, accuracy

---

## Camera

### phone_camera
| Param | Type | Default |
|-------|------|--------|
| camera_id | int | 0 (0=back, 1=front) |

Returns JPEG image.

---

## Hardware

### phone_torch — `{ on: boolean }`
### phone_vibrate — `{ duration_ms: 100-10000, default 500 }`
### phone_tts — `{ text: string, language: string (default en) }`

---

## Volume

### phone_volume_get — No parameters
### phone_volume_set
| Param | Type | Description |
|-------|------|-------------|
| stream | string | music/call/ring/alarm/notification/system |
| value | int | 0-15 |

---

## Apps

### phone_app_list — No parameters
### phone_app_launch
| Param | Type | Default |
|-------|------|--------|
| package | string | required (e.g. com.android.chrome) |
| activity | string | "" |

---

## UI Automation

### phone_tap — `{ x: int, y: int }`
### phone_swipe — `{ x1, y1, x2, y2: int, duration_ms: 300 }`
### phone_type — `{ text: string }`
### phone_key — `{ keycode: string }` (KEYCODE_BACK, KEYCODE_HOME, KEYCODE_ENTER, etc.)
