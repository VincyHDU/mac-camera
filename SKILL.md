# mac-camera

Capture photos and videos from your MacBook camera via OpenClaw.

## Description

This skill enables OpenClaw to control your MacBook's built-in camera (FaceTime HD camera) for capturing photos and recording videos. It uses macOS native tools (`imagesnap` for photos, `ffmpeg` for videos) wrapped in a clean Python interface.

## Activation

Activate this skill when the user mentions:
- "take a photo", "capture picture", "snapshot"
- "record video", "start recording", "video capture"
- "mac camera", "webcam", "FaceTime camera"
- Any request involving the MacBook's built-in camera

## Tools

### `mac_camera_capture`
Capture a photo from the MacBook camera.

**Parameters:**
- `output_path` (optional): Path to save the photo. Default: `photo_YYYYMMDD_HHMMSS.jpg` in current directory.
- `delay` (optional): Warmup delay in seconds before capturing. Default: 1 second.

**Returns:**
Path to the captured photo file.

**Example:**
```python
# Capture a photo with 2-second delay
photo_path = mac_camera_capture(delay=2)
```

### `mac_camera_record`
Record a video from the MacBook camera.

**Parameters:**
- `output_path` (optional): Path to save the video. Default: `video_YYYYMMDD_HHMMSS.mp4` in current directory.
- `duration` (optional): Recording duration in seconds. Default: 10 seconds.
- `resolution` (optional): Video resolution (e.g., "640x480", "1280x720"). Default: "1280x720".

**Returns:**
Path to the recorded video file.

**Example:**
```python
# Record a 15-second video
video_path = mac_camera_record(duration=15, resolution="640x480")
```

### `mac_camera_list_devices`
List available camera devices.

**Returns:**
List of available camera devices with their names.

## Dependencies

This skill requires:
1. `imagesnap` - For photo capture (`brew install imagesnap`)
2. `ffmpeg` - For video recording (`brew install ffmpeg`)

Install with:
```bash
brew install imagesnap ffmpeg
```

## Permissions

macOS requires camera permissions. If you see permission errors:
1. Open **System Settings** > **Privacy & Security** > **Camera**
2. Grant camera access to:
   - Terminal (if running from command line)
   - The app running OpenClaw
   - Python (if running Python scripts directly)

## Safety Notes

- Camera access is sensitive. Always ask for permission before capturing.
- Photos/videos are saved locally by default.
- Consider privacy implications when sharing captured media.
- The skill includes a default delay to give users time to prepare.

## Examples

**Basic photo capture:**
```bash
# When user says: "Take a photo of my desk"
# Skill activates and captures a photo
```

**Video recording:**
```bash
# When user says: "Record a quick 30-second video"
# Skill activates and records a video
```

**With custom settings:**
```bash
# When user says: "Take a high-quality photo for documentation"
# Skill captures with longer delay and higher quality settings
```

## Troubleshooting

**"No camera found" error:**
- Check if `imagesnap -l` lists your camera
- Verify camera permissions in System Settings
- Ensure camera is not in use by another app

**"ffmpeg not found" error:**
- Install ffmpeg: `brew install ffmpeg`
- Verify installation: `ffmpeg -version`

**Permission denied:**
- Grant camera access in System Settings
- Restart the application after granting permissions

## Development

The skill is implemented in `mac_camera.py` with a clean Python API. To extend:
1. Add new methods to `MacCamera` class
2. Update tool definitions in skill configuration
3. Test with `python mac_camera.py --test`

## License

MIT License - See LICENSE file for details.

## GitHub

Repository: [Your GitHub URL here]
Issues: [Your issues URL here]
Contributing: Pull requests welcome!