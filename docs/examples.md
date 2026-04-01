# Example Prompts

## Device Status
- "What is my battery level?" — phone_info
- "What WiFi am I on?" — phone_info
- "How much storage is left?" — phone_shell df -h /sdcard
- "Full status report" — phone_info + phone_screenshot

## Files
- "List my Downloads folder" — phone_file_list /sdcard/Download
- "Read /sdcard/notes.txt" — phone_file_read
- "Create /sdcard/todo.txt" — phone_file_write
- "Count photos in DCIM" — phone_shell ls /sdcard/DCIM/Camera | wc -l

## Screen
- "Take a screenshot and describe it" — phone_screenshot
- "What app am I using?" — phone_screenshot
- "Are there notifications?" — phone_screenshot

## Notifications
- "Send notification: Build complete" — phone_notification
- "Alert: meeting in 5 minutes" — phone_notification
- "What is in my clipboard?" — phone_clipboard_get
- "Copy URL to my phone clipboard" — phone_clipboard_set

## Communication
- "Show last 20 texts" — phone_sms_list limit 20
- "Send SMS: I will be late" — phone_sms_send (real SMS!)
- "List contacts named John" — phone_contacts_list + filter

## Location
- "Where is my phone?" — phone_location gps
- "Quick location" — phone_location network

## Camera
- "Take a photo" — phone_camera camera_id 0
- "Take a selfie" — phone_camera camera_id 1
- "Photo and describe contents" — phone_camera

## Hardware
- "Turn on flashlight" — phone_torch on: true
- "Turn off flashlight" — phone_torch on: false
- "Vibrate my phone" — phone_vibrate
- "Say Hello World" — phone_tts

## Volume
- "Current volume?" — phone_volume_get
- "Max ring volume" — phone_volume_set ring 15
- "Mute media" — phone_volume_set music 0

## Apps
- "What apps are installed?" — phone_app_list
- "Open Spotify" — phone_app_launch com.spotify.music
- "Launch Chrome" — phone_app_launch com.android.chrome
- "Open Settings" — phone_app_launch com.android.settings

## UI Automation
- "Tap center of screen" — phone_screenshot then phone_tap
- "Scroll down" — phone_swipe (540,1500) to (540,500)
- "Press back" — phone_key KEYCODE_BACK
- "Go home" — phone_key KEYCODE_HOME
- "Type Hello" — phone_tap then phone_type

## Multi-step Workflows

**Open Chrome and go to google.com:**
1. phone_app_launch com.android.chrome
2. phone_shell sleep 2
3. phone_screenshot
4. phone_tap address bar
5. phone_type google.com
6. phone_key KEYCODE_ENTER

**Send location via SMS:**
1. phone_location
2. Format as Maps link
3. phone_contacts_list to find number
4. phone_sms_send

**Full phone snapshot:**
1. phone_info
2. phone_screenshot
3. phone_location
4. Claude compiles report
