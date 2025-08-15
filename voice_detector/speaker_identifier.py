from pyannote.audio import Model
import torch
import numpy as np
from scipy.spatial.distance import cdist
from pyannote.core import Segment
import torchaudio

def identify_speaker(diarization, audio_path, reference_path, threshold=0.8):
    """
    Identifies the target speaker in a diarized audio file.

    Args:
        diarization (pyannote.core.Annotation): The diarization result.
        audio_path (str): The path to the main audio file.
        reference_path (str): The path to the reference audio of the target speaker.
        threshold (float): The cosine similarity threshold for matching.

    Returns:
        list: A list of (start, end) tuples for the target speaker's segments.
    """
    try:
        print("Identifying target speaker...")
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        embedding_model = Model.from_pretrained("pyannote/embedding", use_auth_token=True).to(device)

        # Compute reference embedding
        ref_waveform, sample_rate = torchaudio.load(reference_path)
        if sample_rate != 16000:
            ref_waveform = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)(ref_waveform)
        
        with torch.no_grad():
            reference_embedding = embedding_model(ref_waveform.to(device)).mean(dim=0).cpu().numpy()

        # Load main audio
        main_waveform, _ = torchaudio.load(audio_path)

        target_segments = []
        for segment, _, _ in diarization.itertracks(yield_label=True):
            subsegment_waveform = main_waveform[:, int(segment.start * 16000):int(segment.end * 16000)]
            
            if subsegment_waveform.shape[1] == 0:
                continue

            with torch.no_grad():
                segment_embedding = embedding_model(subsegment_waveform.to(device)).mean(dim=0).cpu().numpy()

            distance = cdist([reference_embedding], [segment_embedding], "cosine")[0, 0]

            if distance < threshold:
                target_segments.append((segment.start, segment.end))

        print(f"Found {len(target_segments)} segments for the target speaker.")
        return target_segments
    except Exception as e:
        print(f"Error during speaker identification: {e}")
        raise
