# DescribeVideo

## Description
Analyze and summarize short videos (e.g., 8-second clips) using the xAI Grok-4 API. It works by extracting frames from a video at a configurable interval (default: 2 frames per second), sending each frame to the Grok-4 model for detailed description, and then combining these descriptions into a cohesive summary of the video's content and events. This is particularly useful for sharing video context with LLMs that don't support direct video uploads, by converting videos into AI-interpretable frame-based narratives.

## Features
- Extracts frames from local video files using OpenCV.
- Describes each frame in detail via the xAI Grok-4 API.
- Generates an overall video summary by synthesizing frame descriptions.
- Configurable frame extraction interval for performance optimization.
- Supports MP4 videos (extendable to other formats via OpenCV).

## Installation
1. Clone the repository:
   ```
   git clone https://github.com/haxies/describevideo.git
   cd describevideo
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Obtain an xAI API key from [https://console.x.ai/](https://console.x.ai/) and set it as an environment variable (recommended for security):
   - On Linux/macOS: `export XAI_API_KEY="your_api_key_here"`
   - On Windows: `set XAI_API_KEY=your_api_key_here`
   
   Alternatively, hardcode it in the script (not recommended for shared code).

## Usage
1. Place your video file (e.g., `video.mp4`) in the same directory as the script.

2. Run the script:
   ```
   python describevideo.py
   ```

3. The script will:
   - Extract frames (e.g., 2 per second).
   - Analyze each frame using Grok-4.
   - Output a summary of the video.

Example output:
```
Extracting frames...
Analyzing 16 frames...
Describing frame 1...
...
Summarizing the video...

Video Summary:
[AI-generated summary here]
```

### Customization
- Adjust the frame extraction interval in `extract_frames` (e.g., `interval=0.5` for 2 frames/second).
- Modify prompts in `describe_image` or `summarize_video` for tailored descriptions.

## Requirements
This project requires Python 3.8+ and access to the xAI API (Grok-4 model, which may need a subscription).

## License
MIT License. See [LICENSE](LICENSE) for details.

## Contributing
Pull requests are welcome! For major changes, open an issue first.

## Disclaimer
This tool relies on the xAI API, which may incur costs based on usage. Ensure compliance with xAI's terms. Hardcoding API keys is insecure—use environment variables in production.

---

Below is the `requirements.txt` file content. Save it as `requirements.txt` in your project root.

```
opencv-python
openai
```
