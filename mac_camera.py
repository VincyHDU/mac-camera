#!/usr/bin/env python3
"""
mac-camera: OpenClaw skill for MacBook camera control
Capture photos and videos from your MacBook's built-in camera.
"""

import subprocess
import os
import sys
import time
from pathlib import Path
from typing import Optional, Tuple, List
import json

class MacCamera:
    """Main class for MacBook camera control"""
    
    def __init__(self):
        self.imagesnap_path = self._find_tool("imagesnap")
        self.ffmpeg_path = self._find_tool("ffmpeg")
        
    def _find_tool(self, tool_name: str) -> str:
        """Find a command-line tool in PATH"""
        try:
            result = subprocess.run(["which", tool_name], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                raise Exception(f"{tool_name} not found in PATH. Install with: brew install {tool_name}")
        except Exception as e:
            raise Exception(f"Failed to find {tool_name}: {e}")
    
    def list_devices(self) -> List[str]:
        """List available camera devices"""
        try:
            result = subprocess.run([self.imagesnap_path, "-l"], 
                                  capture_output=True, text=True)
            devices = []
            for line in result.stdout.strip().split('\n'):
                if line.strip() and "devices" not in line.lower():
                    devices.append(line.strip())
            return devices
        except Exception as e:
            print(f"Error listing devices: {e}")
            return []
    
    def capture_photo(self, 
                     output_path: Optional[str] = None, 
                     delay: int = 1,
                     quality: int = 85) -> Optional[str]:
        """
        Capture a photo from the camera
        
        Args:
            output_path: Path to save the photo (default: timestamp.jpg in current dir)
            delay: Warmup delay in seconds before capturing
            quality: JPEG quality (1-100, higher is better)
        
        Returns:
            Path to the captured photo, or None if failed
        """
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"photo_{timestamp}.jpg"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Build command
        cmd = [self.imagesnap_path]
        if delay > 0:
            cmd.extend(["-w", str(delay)])  # Warmup delay
        
        cmd.append(output_path)
        
        print(f"📸 Capturing photo to: {output_path}")
        print(f"   Command: {' '.join(cmd)}")
        print(f"   Delay: {delay}s, Quality: {quality}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Photo captured: {output_path} ({file_size:,} bytes)")
                
                # Optional: compress with sips if quality specified
                if quality < 100:
                    self._compress_image(output_path, quality)
                    
                return output_path
            else:
                print(f"❌ Photo not created. Error: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"❌ Error capturing photo: {e}")
            return None
    
    def _compress_image(self, image_path: str, quality: int):
        """Compress image using macOS sips tool"""
        try:
            temp_path = f"{image_path}.tmp"
            cmd = ["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality),
                   image_path, "--out", temp_path]
            subprocess.run(cmd, capture_output=True)
            
            if os.path.exists(temp_path):
                os.replace(temp_path, image_path)
                new_size = os.path.getsize(image_path)
                print(f"   Compressed to: {new_size:,} bytes (quality: {quality})")
        except Exception as e:
            print(f"   Note: Compression failed: {e}")
    
    def record_video(self,
                    output_path: Optional[str] = None,
                    duration: int = 10,
                    resolution: str = "1280x720",
                    fps: int = 30,
                    audio: bool = False) -> Optional[str]:
        """
        Record a video from the camera
        
        Args:
            output_path: Path to save the video (default: timestamp.mp4)
            duration: Recording duration in seconds
            resolution: Video resolution (e.g., "640x480", "1280x720")
            fps: Frames per second
            audio: Include audio (requires microphone permissions)
        
        Returns:
            Path to the recorded video, or None if failed
        """
        if output_path is None:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"video_{timestamp}.mp4"
        
        # Ensure directory exists
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Get video device (usually 0 for built-in camera)
        video_device = "0"  # Default to first video device
        
        # Build ffmpeg command
        cmd = [
            self.ffmpeg_path,
            "-f", "avfoundation",  # macOS video capture format
            "-framerate", str(fps),
            "-video_size", resolution,
            "-i", f"{video_device}:{0 if audio else 'none'}",  # 0 for default audio device
            "-t", str(duration),  # Duration
            "-c:v", "libx264",  # Video codec
            "-preset", "fast",  # Encoding preset
            "-crf", "23",  # Quality (lower = better)
            "-pix_fmt", "yuv420p",  # Pixel format for compatibility
            "-y",  # Overwrite output file
            output_path
        ]
        
        print(f"🎥 Recording video to: {output_path}")
        print(f"   Duration: {duration}s, Resolution: {resolution}, FPS: {fps}")
        print(f"   Audio: {'Enabled' if audio else 'Disabled'}")
        
        try:
            # Run ffmpeg (it will show progress in stderr)
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 5)
            
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"✅ Video recorded: {output_path} ({file_size:,} bytes)")
                return output_path
            else:
                print(f"❌ Video not created. Error: {result.stderr[:500]}")
                return None
                
        except subprocess.TimeoutExpired:
            print("❌ Recording timed out")
            return None
        except Exception as e:
            print(f"❌ Error recording video: {e}")
            return None
    
    def get_camera_info(self) -> dict:
        """Get information about available cameras"""
        devices = self.list_devices()
        
        info = {
            "imagesnap_available": os.path.exists(self.imagesnap_path),
            "ffmpeg_available": os.path.exists(self.ffmpeg_path),
            "devices": devices,
            "default_resolutions": ["640x480", "1280x720", "1920x1080"],
            "supported_formats": {
                "photos": ["jpg", "jpeg", "png"],
                "videos": ["mp4", "mov", "avi"]
            }
        }
        
        return info

def test_photo_capture():
    """Test photo capture functionality"""
    print("=== Testing Photo Capture ===\n")
    
    try:
        camera = MacCamera()
        print(f"📷 Camera tools found:")
        print(f"   imagesnap: {camera.imagesnap_path}")
        print(f"   ffmpeg: {camera.ffmpeg_path}")
        
        devices = camera.list_devices()
        print(f"\n📱 Available devices: {devices}")
        
        if devices:
            print("\n--- Capturing test photo (2 second delay) ---")
            photo_path = camera.capture_photo(delay=2)
            
            if photo_path:
                return True, photo_path
            else:
                return False, "Failed to capture photo"
        else:
            return False, "No camera devices found"
            
    except Exception as e:
        return False, str(e)

def test_video_recording():
    """Test video recording functionality"""
    print("\n=== Testing Video Recording ===\n")
    
    try:
        camera = MacCamera()
        
        print("--- Recording test video (5 seconds, 640x480) ---")
        video_path = camera.record_video(duration=5, resolution="640x480", audio=False)
        
        if video_path:
            return True, video_path
        else:
            return False, "Failed to record video"
            
    except Exception as e:
        return False, str(e)

def main():
    """Main test function"""
    print("=== mac-camera Skill Test ===\n")
    
    # Test photo capture
    photo_success, photo_result = test_photo_capture()
    
    # Test video recording (if photo worked)
    video_success = False
    video_result = "Skipped"
    
    if photo_success:
        video_success, video_result = test_video_recording()
    
    # Summary
    print("\n=== Test Summary ===")
    print(f"Photo capture: {'✅ PASS' if photo_success else '❌ FAIL'}")
    if photo_success:
        print(f"   Photo saved: {photo_result}")
    else:
        print(f"   Error: {photo_result}")
    
    print(f"Video recording: {'✅ PASS' if video_success else '❌ FAIL'}")
    if video_success:
        print(f"   Video saved: {video_result}")
    else:
        print(f"   Error: {video_result}")
    
    # Camera info
    try:
        camera = MacCamera()
        info = camera.get_camera_info()
        print(f"\n📊 Camera Info:")
        print(f"   Devices: {info['devices']}")
        print(f"   Available tools: imagesnap={info['imagesnap_available']}, ffmpeg={info['ffmpeg_available']}")
    except:
        pass
    
    # Recommendations
    print("\n💡 Recommendations:")
    if not photo_success:
        print("1. Check camera permissions in System Settings > Privacy & Security > Camera")
        print("2. Make sure imagesnap is installed: brew install imagesnap")
        print("3. Try running manually: imagesnap test.jpg")
    
    if not video_success and photo_success:
        print("1. Install ffmpeg: brew install ffmpeg")
        print("2. Check ffmpeg version: ffmpeg -version")
    
    return 0 if (photo_success or video_success) else 1

if __name__ == "__main__":
    sys.exit(main())