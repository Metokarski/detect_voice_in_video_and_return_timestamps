from pyannote.audio import Pipeline
import torch

def run_diarization(audio_path, hf_token):
    """
    Performs speaker diarization on an audio file.

    Args:
        audio_path (str): The path to the input audio file.
        hf_token (str): The Hugging Face API token.

    Returns:
        pyannote.core.Annotation: The diarization result.
    """
    try:
        print("Running speaker diarization...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=hf_token
        ).to(device)
        
        diarization = pipeline(audio_path)
        print("Diarization complete.")
        return diarization
    except Exception as e:
        print(f"Error during diarization: {e}")
        raise
