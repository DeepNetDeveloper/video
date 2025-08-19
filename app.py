import os
import sys
import gradio as gr
import subprocess
import tempfile
import shutil
import random
from pathlib import Path

# Add the current directory to the path to import utils
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def process_video_retalking(
    face_input,
    audio_input,
    exp_img,
    fps,
    pads_top,
    pads_bottom,
    pads_left,
    pads_right,
    face_det_batch_size,
    lnet_batch_size,
    img_size,
    crop_top,
    crop_bottom,
    crop_left,
    crop_right,
    box_top,
    box_bottom,
    box_left,
    box_right,
    nosmooth,
    static,
    up_face,
    one_shot,
    without_rl1,
    re_preprocess,
    progress=gr.Progress()
):
    """
    Process video with retalking using all available options
    """
    
    if not face_input or not audio_input:
        return None, "Please provide both face and audio inputs"
    
    try:
        # Create output directory
        os.makedirs("results", exist_ok=True)
        
        # Generate unique output filename
        output_filename = f"results/output_{random.randint(10000, 99999)}.mp4"
        
        # Build command arguments
        cmd = [
            "python", "inference.py",
            "--face", face_input,
            "--audio", audio_input,
            "--outfile", output_filename
        ]
        
        # Add optional arguments with non-default values
        if exp_img != "neutral":
            cmd.extend(["--exp_img", exp_img])
        
        if fps != 25.0:
            cmd.extend(["--fps", str(fps)])
        
        # Handle pads (default: [0, 20, 0, 0])
        pads = [pads_top, pads_bottom, pads_left, pads_right]
        if pads != [0, 20, 0, 0]:
            cmd.extend(["--pads"] + [str(p) for p in pads])
        
        if face_det_batch_size != 4:
            cmd.extend(["--face_det_batch_size", str(face_det_batch_size)])
        
        if lnet_batch_size != 16:
            cmd.extend(["--LNet_batch_size", str(lnet_batch_size)])
        
        if img_size != 384:
            cmd.extend(["--img_size", str(img_size)])
        
        # Handle crop (default: [0, -1, 0, -1])
        crop = [crop_top, crop_bottom, crop_left, crop_right]
        if crop != [0, -1, 0, -1]:
            cmd.extend(["--crop"] + [str(c) for c in crop])
        
        # Handle box (default: [-1, -1, -1, -1])
        box = [box_top, box_bottom, box_left, box_right]
        if box != [-1, -1, -1, -1]:
            cmd.extend(["--box"] + [str(b) for b in box])
        
        if nosmooth:
            cmd.append("--nosmooth")
        
        if static:
            cmd.append("--static")
        
        if up_face != "original":
            cmd.extend(["--up_face", up_face])
        
        if one_shot:
            cmd.append("--one_shot")
        
        if without_rl1:
            cmd.append("--without_rl1")
        
        if re_preprocess:
            cmd.append("--re_preprocess")
        
        # Run the inference
        progress(0.1, desc="Starting video processing...")
        
        print("Running command:", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=current_dir)
        
        progress(0.9, desc="Finalizing output...")
        
        if result.returncode == 0:
            progress(1.0, desc="Processing complete!")
            if os.path.exists(output_filename):
                return output_filename, "Video processing completed successfully!"
            else:
                return None, f"Processing completed but output file not found. Command output: {result.stdout}\nError: {result.stderr}"
        else:
            error_msg = f"Error processing video:\nCommand: {' '.join(cmd)}\nReturn code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            print(error_msg)
            return None, error_msg
    
    except Exception as e:
        error_msg = f"Exception occurred: {str(e)}"
        print(error_msg)
        return None, error_msg

def reset_to_defaults():
    """Reset all parameters to their default values"""
    return (
        None,  # face_input
        None,  # audio_input
        "neutral",  # exp_img
        25.0,  # fps
        0,  # pads_top
        20,  # pads_bottom
        0,  # pads_left
        0,  # pads_right
        4,  # face_det_batch_size
        16,  # lnet_batch_size
        384,  # img_size
        0,  # crop_top
        -1,  # crop_bottom
        0,  # crop_left
        -1,  # crop_right
        -1,  # box_top
        -1,  # box_bottom
        -1,  # box_left
        -1,  # box_right
        False,  # nosmooth
        False,  # static
        "original",  # up_face
        False,  # one_shot
        False,  # without_rl1
        False,  # re_preprocess
    )

# Create the Gradio interface
with gr.Blocks(
    title="Video Retalking - Complete Interface",
    theme=gr.themes.Soft(
        primary_hue=gr.themes.colors.blue,
        secondary_hue=gr.themes.colors.gray,
        font=["Source Sans Pro", "Arial", "sans-serif"],
    ),
) as app:
    
    gr.Markdown("# 🎬 Video Retalking - Complete Interface")
    gr.Markdown("Generate lip-synchronized videos with comprehensive control over all parameters.")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 📁 Input Files")
            
            face_input = gr.Video(
                label="Face Video/Image"
            )
            
            audio_input = gr.Audio(
                label="Audio Source",
                type="filepath"
            )
            
            gr.Markdown("## 🎭 Expression Control")
            
            exp_img = gr.Dropdown(
                choices=["neutral", "smile", "sad", "angry", "surprise"],
                value="neutral",
                label="Expression Template"
            )
            
            gr.Markdown("## ⚙️ Basic Settings")
            
            fps = gr.Number(
                value=25.0,
                label="FPS",
                minimum=1.0,
                maximum=60.0
            )
            
            up_face = gr.Dropdown(
                choices=["original", "sad", "angry", "surprise"],
                value="original",
                label="Face Enhancement"
            )
            
        with gr.Column(scale=1):
            gr.Markdown("## 🔧 Advanced Parameters")
            
            with gr.Accordion("Padding Settings", open=False):
                gr.Markdown("Adjust padding around the face (top, bottom, left, right)")
                with gr.Row():
                    pads_top = gr.Number(value=0, label="Top", minimum=0, maximum=100)
                    pads_bottom = gr.Number(value=20, label="Bottom", minimum=0, maximum=100)
                with gr.Row():
                    pads_left = gr.Number(value=0, label="Left", minimum=0, maximum=100)
                    pads_right = gr.Number(value=0, label="Right", minimum=0, maximum=100)
            
            with gr.Accordion("Batch & Performance", open=False):
                face_det_batch_size = gr.Slider(
                    minimum=1, maximum=32, value=4, step=1,
                    label="Face Detection Batch Size"
                )
                
                lnet_batch_size = gr.Slider(
                    minimum=1, maximum=64, value=16, step=1,
                    label="LNet Batch Size"
                )
                
                img_size = gr.Dropdown(
                    choices=[256, 384, 512],
                    value=384,
                    label="Image Size"
                )
            
            with gr.Accordion("Crop Settings", open=False):
                gr.Markdown("Crop video region (top, bottom, left, right). -1 means auto-infer")
                with gr.Row():
                    crop_top = gr.Number(value=0, label="Crop Top")
                    crop_bottom = gr.Number(value=-1, label="Crop Bottom")
                with gr.Row():
                    crop_left = gr.Number(value=0, label="Crop Left")
                    crop_right = gr.Number(value=-1, label="Crop Right")
            
            with gr.Accordion("Face Bounding Box (Advanced)", open=False):
                gr.Markdown("Manual face detection box (use only if automatic detection fails)")
                with gr.Row():
                    box_top = gr.Number(value=-1, label="Box Top")
                    box_bottom = gr.Number(value=-1, label="Box Bottom")
                with gr.Row():
                    box_left = gr.Number(value=-1, label="Box Left")
                    box_right = gr.Number(value=-1, label="Box Right")
            
            with gr.Accordion("Processing Options", open=False):
                nosmooth = gr.Checkbox(
                    label="No Smoothing",
                    value=False
                )
                
                static = gr.Checkbox(
                    label="Static Mode",
                    value=False
                )
                
                one_shot = gr.Checkbox(
                    label="One Shot",
                    value=False
                )
                
                without_rl1 = gr.Checkbox(
                    label="Without Relative L1",
                    value=False
                )
                
                re_preprocess = gr.Checkbox(
                    label="Re-preprocess",
                    value=False
                )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 🎬 Examples")
            
            # Face examples
            face_examples = []
            face_examples_dir = os.path.join(current_dir, "examples", "face")
            if os.path.exists(face_examples_dir):
                for i in range(1, 6):
                    example_path = os.path.join(face_examples_dir, f"{i}.mp4")
                    if os.path.exists(example_path):
                        face_examples.append(example_path)
            
            if face_examples:
                gr.Examples(
                    examples=[[example] for example in face_examples[:3]],
                    inputs=[face_input],
                    label="Face Examples"
                )
            
            # Audio examples
            audio_examples = []
            audio_examples_dir = os.path.join(current_dir, "examples", "audio")
            if os.path.exists(audio_examples_dir):
                for i in range(1, 3):
                    example_path = os.path.join(audio_examples_dir, f"{i}.wav")
                    if os.path.exists(example_path):
                        audio_examples.append(example_path)
            
            if audio_examples:
                gr.Examples(
                    examples=[[example] for example in audio_examples],
                    inputs=[audio_input],
                    label="Audio Examples"
                )
        
        with gr.Column():
            gr.Markdown("## 🎯 Controls")
            
            with gr.Row():
                process_btn = gr.Button(
                    "🚀 Generate Video",
                    variant="primary",
                    size="lg"
                )
                reset_btn = gr.Button(
                    "🔄 Reset to Defaults",
                    variant="secondary"
                )
            
            status_text = gr.Textbox(
                label="Status",
                interactive=False,
                placeholder="Ready to process..."
            )
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("## 📹 Output")
            output_video = gr.Video(label="Generated Video")
    
    # Collect all input components for easy handling
    all_inputs = [
        face_input, audio_input, exp_img, fps,
        pads_top, pads_bottom, pads_left, pads_right,
        face_det_batch_size, lnet_batch_size, img_size,
        crop_top, crop_bottom, crop_left, crop_right,
        box_top, box_bottom, box_left, box_right,
        nosmooth, static, up_face, one_shot, without_rl1, re_preprocess
    ]
    
    # Button click handlers
    process_btn.click(
        fn=process_video_retalking,
        inputs=all_inputs,
        outputs=[output_video, status_text],
        show_progress=True
    )
    
    reset_btn.click(
        fn=reset_to_defaults,
        outputs=all_inputs
    )
    
    # Add footer information
    gr.Markdown("""
    ---
    ### 📝 Parameter Guide:
    - **Expression Template**: Choose predefined expressions or use custom image path
    - **Padding**: Adjust space around detected face (helps include chin/forehead)
    - **Crop Settings**: Define region of interest in input video
    - **Batch Sizes**: Higher values = faster processing but more memory usage
    - **One Shot**: Uses first frame as reference for consistent appearance
    - **No Smoothing**: Disables temporal smoothing of face detection
    - **Re-preprocess**: Forces regeneration of cached intermediate files
    
    ### 🚀 Quick Start:
    1. Upload a face video/image and audio file
    2. Adjust expression template if desired
    3. Click "Generate Video" 
    4. Use "Reset to Defaults" to restore all settings
    """)

if __name__ == "__main__":
    # Ensure required directories exist
    os.makedirs("temp", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    app.queue(max_size=3).launch(
        share=True,
        show_error=True
    )
