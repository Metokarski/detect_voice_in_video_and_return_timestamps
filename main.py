import argparse
import os
from dotenv import load_dotenv
from voice_detector.audio_extractor import extract_audio
from voice_detector.diarizer import run_diarization
from voice_detector.speaker_identifier import identify_speaker
from voice_detector.utils import save_timestamps_to_csv, merge_segments

def main():
    load_dotenv()
    hf_token = os.getenv("HF_TOKEN")

    if not hf_token:
        print("Error: Hugging Face token not found.")
        print("Please create a .env file and add your HF_TOKEN.")
        return

    parser = argparse.ArgumentParser(description="Detect a specific person's voice in a video.")
    parser.add_argument("--video_path", required=True, help="Path to the input video file.")
    parser.add_argument("--reference_path", required=True, help="Path to the reference audio file (WAV).")
    parser.add_argument("--output_path", required=True, help="Path to save the output CSV file.")
    parser.add_argument("--threshold", type=float, default=0.8, help="Cosine similarity threshold.")
    parser.add_argument("--no-merge", action="store_true", help="Do not merge adjacent segments.")


    args = parser.parse_args()

    temp_audio_path = "temp_audio.wav"

    try:
        # 1. Extract audio
        extract_audio(args.video_path, temp_audio_path)

        # 2. Run diarization
        diarization = run_diarization(temp_audio_path, hf_token)

        # 3. Identify speaker
        target_segments = identify_speaker(
            diarization,
            temp_audio_path,
            args.reference_path,
            args.threshold
        )
        
        # 4. Merge segments
        if not args.no_merge:
            print("Merging segments...")
            target_segments = merge_segments(target_segments)


        # 5. Save timestamps
        save_timestamps_to_csv(target_segments, args.output_path)

    finally:
        # Clean up temporary audio file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)

if __name__ == "__main__":
    main()
