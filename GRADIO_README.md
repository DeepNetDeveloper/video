# Video Retalking - Gradio Web Interface

This is a comprehensive Gradio web interface for the Video Retalking project, providing access to all available parameters and options through an intuitive web UI.

## 🚀 Quick Start

### Option 1: Using the Launcher (Recommended)
```bash
python launch_app.py
```

### Option 2: Direct Launch
```bash
python app.py
```

The web interface will be available at: `http://localhost:7860`

## 📋 Features

### Core Functionality
- **Face Input**: Upload video or image containing the face to animate
- **Audio Input**: Upload audio file for lip synchronization
- **Expression Control**: Choose from predefined expressions (neutral, smile, sad, angry, surprise)
- **Real-time Processing**: Monitor progress with live updates

### Advanced Parameters

#### 🎭 Expression & Enhancement
- **Expression Template**: Predefined expressions or custom image paths
- **Face Enhancement**: Apply facial expression modifications
- **One Shot Mode**: Use first frame as reference for consistency

#### ⚙️ Processing Settings
- **FPS Control**: Adjust frame rate for static images
- **Image Size**: Choose processing resolution (256/384/512)
- **Batch Sizes**: Optimize performance vs memory usage
- **Static Mode**: Process single images

#### 🔧 Fine-tuning Options
- **Padding**: Adjust space around detected face
- **Crop Settings**: Define region of interest
- **Face Bounding Box**: Manual face detection override
- **Smoothing Control**: Enable/disable temporal smoothing
- **Preprocessing**: Force regeneration of cached data

## 🎯 Parameter Guide

### Basic Parameters
| Parameter | Default | Description |
|-----------|---------|-------------|
| Expression Template | neutral | Predefined expressions or custom image |
| FPS | 25.0 | Frames per second (for static images) |
| Face Enhancement | original | Apply expression enhancements |

### Padding Settings (Default: [0, 20, 0, 0])
- **Top/Bottom/Left/Right**: Adjust space around face
- **Tip**: Increase bottom padding to include chin

### Batch & Performance
| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Face Detection Batch Size | 4 | 1-32 | Higher = faster but more memory |
| LNet Batch Size | 16 | 1-64 | Lip-sync network batch size |
| Image Size | 384 | 256/384/512 | Processing resolution |

### Crop Settings (Default: [0, -1, 0, -1])
- **Crop values**: Define video region to process
- **-1**: Auto-infer based on video dimensions
- **Use case**: Multiple faces in video

### Advanced Options
- **No Smoothing**: Disable face detection temporal smoothing
- **Static Mode**: Process as single image
- **One Shot**: Use first frame as reference for all frames
- **Without Relative L1**: Disable relative L1 loss
- **Re-preprocess**: Force regeneration of cached intermediate files

## 📁 File Structure

```
├── app.py                 # Main Gradio application
├── launch_app.py         # Launcher script with checks
├── inference.py          # Core inference engine
├── requirements.txt      # Python dependencies
├── checkpoints/          # Model checkpoints
├── examples/            # Sample files
│   ├── face/           # Face video examples
│   └── audio/          # Audio examples
├── temp/               # Temporary processing files
└── results/            # Generated videos
```

## 🔄 Workflow

1. **Upload Files**: Add face video/image and audio file
2. **Configure**: Adjust parameters as needed (defaults work well)
3. **Process**: Click "Generate Video" 
4. **Download**: Get your lip-synced video from the output section
5. **Reset**: Use "Reset to Defaults" to restore all settings

## 💡 Tips & Best Practices

### For Best Results
- **Face Quality**: Use high-quality face videos with clear facial features
- **Audio Quality**: Ensure audio is clear with minimal background noise
- **Lighting**: Well-lit faces produce better results
- **Face Size**: Faces should be reasonably large in the frame

### Performance Optimization
- **Batch Sizes**: Start with defaults, increase if you have more GPU memory
- **Image Size**: Use 384 for balance, 512 for quality, 256 for speed
- **One Shot**: Enable for consistent appearance across frames

### Troubleshooting
- **Face Not Detected**: Try manual bounding box settings
- **Poor Quality**: Increase image size or adjust padding
- **Memory Issues**: Reduce batch sizes
- **Processing Errors**: Enable re-preprocess to clear cache

## 🛠️ Development

### Adding New Features
The app is designed to be easily extensible:

1. **New Parameters**: Add to `process_video_retalking()` function
2. **UI Components**: Add Gradio components in the interface section
3. **Validation**: Add parameter validation as needed

### Custom Expressions
To add custom expressions:
1. Place expression image in accessible directory
2. Use file path in Expression Template dropdown
3. Or extend the dropdown choices in the code

## 📝 Dependencies

Core requirements:
- `gradio>=3.7.0` - Web interface
- `torch` - Deep learning framework
- `opencv-python` - Computer vision
- `numpy` - Numerical computing

See `requirements.txt` for complete list.

## 🆘 Support

### Common Issues
1. **Missing Checkpoints**: Download all required model files
2. **Import Errors**: Install requirements with `pip install -r requirements.txt`
3. **CUDA Issues**: Ensure PyTorch CUDA version matches your system
4. **Memory Errors**: Reduce batch sizes or image resolution

### Getting Help
- Check console output for detailed error messages
- Verify all model checkpoints are present
- Ensure input files are in supported formats
- Try with example files first

## 🎬 Examples

The interface includes example files:
- **Face Examples**: Sample face videos in `examples/face/`
- **Audio Examples**: Sample audio files in `examples/audio/`

Click on examples to automatically load them into the interface.

## 🔒 Security Notes

- The app runs locally by default
- Set `share=True` in `app.py` for public access (use with caution)
- Temporary files are stored in `temp/` directory
- Generated videos are saved in `results/` directory

---

Enjoy creating amazing lip-synced videos! 🎉