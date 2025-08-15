import ffmpeg
import os

def extract_audio(video_path, output_audio_path):
    """
    Extracts audio from a video file and saves it as a WAV file.

    Args:
        video_path (str): The path to the input video file.
        output_audio_path (str): The path to save the output WAV file.
    """
    try:
        print(f"Extracting audio from {video_path}...")
        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, ac=1, ar=16000, f='wav')
            .run(overwrite_output=True, quiet=True)
        )
        print(f"Audio extracted and saved to {output_audio_path}")
    except ffmpeg.Error as e:
        print(f"Error extracting audio: {e.stderr.decode()}")
        raise
