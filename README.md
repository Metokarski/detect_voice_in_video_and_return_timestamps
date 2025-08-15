# Voice Activity Detection and Speaker Identification

This repository provides a tool to detect a specific person's voice in a video and return the timestamps of their speech segments. It uses `pyannote.audio` for speaker diarization and a custom speaker identification module to find the target speaker.

## Features

-   Extracts audio from a video file.
-   Performs speaker diarization to identify who spoke when.
-   Identifies a target speaker using a reference audio clip.
-   Outputs timestamps for the target speaker's speech segments.
-   Fully automated via a single command-line script.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/voice-activity-detection.git
    cd voice-activity-detection
    ```

2.  **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set up your Hugging Face API token:**

    -   Create a `.env` file by copying the example:
        ```bash
        cp .env.example .env
        ```
    -   Get a Hugging Face token with read access to `pyannote/speaker-diarization-3.1`. You can create one [here](https://huggingface.co/settings/tokens).
    -   Open the `.env` file and replace `"YOUR_HUGGING_FACE_TOKEN"` with your actual token.

## Usage

Place your input video and the target speaker's reference audio clip in a directory (e.g., `samples/`).

Run the main script with the following command:

```bash
python main.py --video_path /path/to/your/video.mp4 --reference_path /path/to/your/reference.wav --output_path /path/to/your/timestamps.csv
```

### Arguments

-   `--video_path`: Path to the input video file.
-   `--reference_path`: Path to the reference audio file (WAV format) of the target speaker.
-   `--output_path`: Path to save the output CSV file with timestamps.
-   `--threshold` (optional): Cosine similarity threshold for speaker matching. Defaults to `0.8`.

### Example

```bash
python main.py --video_path samples/input.mp4 --reference_path samples/target_speaker.wav --output_path output/timestamps.csv
```

This will create a `timestamps.csv` file in the `output` directory with the start and end times of the target speaker's speech.
