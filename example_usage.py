#!/usr/bin/env python3
"""
Example usage of the mac-camera OpenClaw skill
"""

from mac_camera import MacCamera
import time

def main():
    print("=== mac-camera Example Usage ===\n")
    
    try:
        # Initialize the camera
        print("1. Initializing camera...")
        camera = MacCamera()
        print(f"   ✅ Camera tools ready\n")
        
        # List available devices
        print("2. Listing camera devices...")
        devices = camera.list_devices()
        if devices:
            for device in devices:
                print(f"   📷 {device}")
        else:
            print("   ❌ No camera devices found")
            return
        
        print()
        
        # Get camera information
        print("3. Camera information:")
        info = camera.get_camera_info()
        print(f"   📊 Imagesnap available: {info['imagesnap_available']}")
        print(f"   📊 FFmpeg available: {info['ffmpeg_available']}")
        print(f"   📊 Supported resolutions: {info['default_resolutions']}")
        
        print("\n" + "="*50 + "\n")
        
        # Example 1: Quick photo capture
        print("📸 Example 1: Quick Photo Capture")
        print("   This will take a photo with 2-second delay...")
        time.sleep(1)
        
        photo_path = camera.capture_photo(delay=2)
        if photo_path:
            print(f"   ✅ Photo saved: {photo_path}")
        else:
            print("   ❌ Photo capture failed")
        
        print("\n" + "="*50 + "\n")
        
        # Example 2: Video recording (optional - uncomment to test)
        print("🎥 Example 2: Video Recording (commented out)")
        print("   Uncomment the code below to test video recording")
        """
        print("   Recording a 3-second test video...")
        video_path = camera.record_video(duration=3, resolution="640x480")
        if video_path:
            print(f"   ✅ Video saved: {video_path}")
        else:
            print("   ❌ Video recording failed")
        """
        
        print("\n" + "="*50 + "\n")
        
        # Example 3: Custom settings
        print("⚙️ Example 3: Custom Settings")
        print("   You can customize various settings:")
        print("   - camera.capture_photo(delay=5, quality=95)")
        print("   - camera.record_video(duration=60, resolution='1920x1080', fps=60)")
        print("   - camera.record_video(duration=10, audio=True)")
        
        print("\n" + "="*50 + "\n")
        
        print("✅ Examples complete!")
        print("\nFor OpenClaw integration:")
        print("1. Copy the mac-camera directory to OpenClaw skills folder")
        print("2. OpenClaw will automatically activate when you mention:")
        print("   - 'take a photo', 'record video', 'mac camera', etc.")
        print("3. Check SKILL.md for complete documentation")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()