import cv2
import base64
import os
import json
from openai import OpenAI
import concurrent.futures
from tqdm import tqdm

# Load configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Initialize the OpenAI client with xAI base URL
client = OpenAI(
    api_key=config['api_key'],
    base_url=config['base_url'],
)

def extract_frames(video_path, interval):
    """
    Extract frames from the video at the given interval (in seconds).
    Returns a list of base64 encoded images.
    Also saves the frames as JPEG files in a 'frames' directory.
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Error opening video file.")
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    frame_count = 0
    extracted_count = 0
    success, image = cap.read()
    
    # Create 'frames' directory if it doesn't exist
    os.makedirs('frames', exist_ok=True)
    
    while success:
        # Extract frame every 'interval' seconds
        if frame_count % int(fps * interval) == 0:
            # Save the frame as JPEG
            frame_filename = f"frames/frame_{extracted_count:03d}.jpg"
            cv2.imwrite(frame_filename, image)
            print(f"Saved frame: {frame_filename}")
            
            # Convert image to JPEG bytes for base64
            _, buffer = cv2.imencode('.jpg', image)
            base64_image = base64.b64encode(buffer).decode('utf-8')
            frames.append(base64_image)
            
            extracted_count += 1
        
        success, image = cap.read()
        frame_count += 1
    
    cap.release()
    return frames

def describe_image(base64_image):
    """
    Send the base64 image to the Grok API for description.
    """
    response = client.chat.completions.create(
        model=config['model'],
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": config['describe_prompt']},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        max_tokens=config['describe_max_tokens'],  # Adjust as needed in config
    )
    return response.choices[0].message.content

def summarize_video(descriptions):
    """
    Summarize the video based on the frame descriptions.
    """
    combined_text = "\n".join([f"Frame {i+1}: {desc}" for i, desc in enumerate(descriptions)])
    prompt = config['summarize_prompt'].format(combined_text=combined_text)
    
    response = client.chat.completions.create(
        model=config['model'],
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=config['summarize_max_tokens'],  # Adjust as needed in config
    )
    return response.choices[0].message.content

# Main function
def describe_video(video_path, interval, max_workers):
    print("Extracting frames...")
    frames = extract_frames(video_path, interval)
    
    print(f"Analyzing...")
    
    # Use multithreading to describe frames in parallel with progress bar
    descriptions = [None] * len(frames)  # Placeholder to preserve order
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_index = {executor.submit(describe_image, frame): i for i, frame in enumerate(frames)}
        with tqdm(total=len(frames), desc="Analyzing frames") as pbar:
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    descriptions[index] = future.result()
                except Exception as e:
                    print(f"Error in frame {index + 1}: {e}")
                pbar.update(1)
    
    print("Summarizing the video...")
    summary = summarize_video(descriptions)
    
    return summary

# Example usage
if __name__ == "__main__":
    try:
        video_summary = describe_video(
            config['video_path'],
            config['frame_interval'],
            config['max_workers']
        )
        print("\nVideo Summary:\n")
        print(video_summary)
    except Exception as e:
        print(f"Error: {e}")