# mac-camera OpenClaw Skill

Capture photos and videos from your MacBook camera directly through OpenClaw.

## Features

- **Photo Capture**: Take photos from your MacBook's built-in camera
- **Video Recording**: Record videos with customizable duration and resolution
- **Device Listing**: See available camera devices
- **Quality Control**: Adjust photo quality and video settings
- **Easy Integration**: Simple Python API for OpenClaw skills

## Installation

### 1. Install Dependencies

```bash
# Install required macOS tools
brew install imagesnap ffmpeg
```

### 2. Install the Skill

```bash
# Clone the repository
git clone https://github.com/yourusername/mac-camera.git
cd mac-camera

# Copy to OpenClaw skills directory (adjust path as needed)
cp -r mac-camera ~/.openclaw/skills/
```

### 3. Grant Camera Permissions

macOS requires camera access. Go to:
- **System Settings** > **Privacy & Security** > **Camera**
- Grant access to:
  - Terminal (if running from command line)
  - The app running OpenClaw
  - Python (if running Python scripts directly)

## Usage

### As an OpenClaw Skill

Once installed, OpenClaw will automatically activate this skill when you mention:
- "take a photo", "capture picture", "snapshot"
- "record video", "start recording", "video capture"
- "mac camera", "webcam", "FaceTime camera"

### Direct Python Usage

```python
from mac_camera import MacCamera

# Initialize camera
camera = MacCamera()

# List available devices
devices = camera.list_devices()
print(f"Available cameras: {devices}")

# Capture a photo
photo_path = camera.capture_photo(delay=2)  # 2-second delay
print(f"Photo saved: {photo_path}")

# Record a video
video_path = camera.record_video(duration=10, resolution="1280x720")
print(f"Video saved: {video_path}")
```

### Command Line Testing

```bash
# Run the test script
python mac_camera.py

# Test photo capture only
python -c "from mac_camera import MacCamera; c = MacCamera(); print(c.capture_photo(delay=1))"
```

## API Reference

### `MacCamera` Class

#### `capture_photo(output_path=None, delay=1, quality=85)`
Capture a photo from the camera.

- `output_path`: Optional custom path (default: `photo_YYYYMMDD_HHMMSS.jpg`)
- `delay`: Warmup delay in seconds before capturing
- `quality`: JPEG quality (1-100, higher is better)

#### `record_video(output_path=None, duration=10, resolution="1280x720", fps=30, audio=False)`
Record a video from the camera.

- `output_path`: Optional custom path (default: `video_YYYYMMDD_HHMMSS.mp4`)
- `duration`: Recording duration in seconds
- `resolution`: Video resolution (e.g., "640x480", "1280x720")
- `fps`: Frames per second
- `audio`: Include audio (requires microphone permissions)

#### `list_devices()`
List available camera devices.

#### `get_camera_info()`
Get detailed information about available cameras and capabilities.

## Examples

### Basic Photo Capture
```python
from mac_camera import MacCamera

camera = MacCamera()
photo = camera.capture_photo(delay=3)  # 3-second countdown
```

### Quick Video Recording
```python
from mac_camera import MacCamera

camera = MacCamera()
video = camera.record_video(duration=5, resolution="640x480")
```

### Custom Settings
```python
from mac_camera import MacCamera

camera = MacCamera()

# High-quality photo
photo = camera.capture_photo(
    output_path="documentation_shot.jpg",
    delay=5,
    quality=95
)

# HD video with audio
video = camera.record_video(
    output_path="presentation.mp4",
    duration=60,
    resolution="1920x1080",
    fps=60,
    audio=True
)
```

## Troubleshooting

### Common Issues

**"imagesnap not found"**
```bash
brew install imagesnap
```

**"ffmpeg not found"**
```bash
brew install ffmpeg
```

**"No camera devices found"**
1. Check camera permissions in System Settings
2. Ensure camera is not in use by another app
3. Try: `imagesnap -l` to list devices manually

**Permission denied errors**
- Grant camera access in System Settings > Privacy & Security > Camera
- Restart your terminal/application after granting permissions

**Video recording fails**
- Ensure ffmpeg is installed: `ffmpeg -version`
- Try lower resolution: `resolution="640x480"`
- Check available cameras: `imagesnap -l`

## Development

### Project Structure
```
mac-camera/
├── SKILL.md              # OpenClaw skill definition
├── mac_camera.py         # Main Python implementation
├── README.md             # This file
├── LICENSE               # MIT License
└── examples/             # Usage examples
```

### Running Tests
```bash
# Run the built-in test
python mac_camera.py

# Manual testing
python -c "from mac_camera import MacCamera; c = MacCamera(); print(c.get_camera_info())"
```

### Extending the Skill
1. Add new methods to `MacCamera` class
2. Update `SKILL.md` with new tool definitions
3. Test thoroughly with different camera devices
4. Update documentation

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

- Open an issue on GitHub for bug reports
- Check the troubleshooting section for common solutions
- Ensure all dependencies are installed and permissions granted

## Acknowledgments

- Uses `imagesnap` for photo capture on macOS
- Uses `ffmpeg` for video recording
- Built for OpenClaw AI assistant platform