#!/usr/bin/env python3
"""
Launch script for Video Retalking Gradio App
Run this script to start the web interface
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import gradio
        import torch
        import cv2
        import numpy as np
        print("✅ Basic requirements check passed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return False

def check_checkpoints():
    """Check if model checkpoints exist"""
    checkpoint_dir = Path("checkpoints")
    required_files = [
        "DNet.pt",
        "LNet.pth", 
        "ENet.pth",
        "face3d_pretrain_epoch_20.pth",
        "GFPGANv1.3.pth",
        "GPEN-BFR-512.pth",
        "RetinaFace-R50.pth",
        "shape_predictor_68_face_landmarks.dat"
    ]
    
    missing_files = []
    for file in required_files:
        if not (checkpoint_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing checkpoint files:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPlease download the required model checkpoints.")
        return False
    else:
        print("✅ Model checkpoints found")
        return True

def main():
    print("🎬 Video Retalking - Gradio App Launcher")
    print("=" * 50)
    
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"📁 Working directory: {script_dir}")
    
    # Check requirements
    if not check_requirements():
        return 1
    
    # Check checkpoints
    if not check_checkpoints():
        print("\n💡 Tip: Make sure you have downloaded all required model files")
        print("   Check the README.md for download instructions")
        return 1
    
    # Create necessary directories
    os.makedirs("temp", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    print("✅ Directories prepared")
    
    # Launch the app
    print("\n🚀 Starting Gradio interface...")
    print("📱 Open your web browser and go to: http://localhost:7860")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Check if we're in a conda environment
        import platform
        if platform.system() == "Windows":
            # For Windows, use conda run command
            cmd = ["conda", "run", "--name", "retalking", "python", "app.py"]
        else:
            # For Unix-like systems
            cmd = ["conda", "run", "--name", "retalking", "python", "app.py"]
        
        # Run the app
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running app: {e}")
        return 1
    except FileNotFoundError:
        print("❌ app.py not found. Make sure you're in the correct directory.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)