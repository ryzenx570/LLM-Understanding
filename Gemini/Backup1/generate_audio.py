import os
import json
import subprocess

# Ensure audio directory exists
os.makedirs("audio", exist_ok=True)

with open('scripts.json', 'r', encoding='utf-8') as f:
    scripts = json.load(f)

# Using Ava
VOICE = "en-US-AvaMultilingualNeural" 

for key, text in scripts.items():
    out_path = f"audio/{key}.mp3"
    # Force overwrite for new voice
        
    print(f"Generating high-quality neural audio for: {key}...")
    
    # edge-tts --voice en-GB-RyanNeural --text "Hello world" --write-media out.mp3
    cmd = [
        "python", "-m", "edge_tts",
        "--voice", VOICE,
        "--rate", "+5%", 
        "--text", text,
        "--write-media", out_path
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"  -> Saved {out_path}")
    except subprocess.CalledProcessError as e:
        print(f"  -> Edge-TTS Error: {e.stderr.decode()}")
    except Exception as e:
        print(f"  -> Exception: {e}")

print("\nFinished generating audio!")
