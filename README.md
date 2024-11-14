# Speech to Text Service

A FastAPI service that transcribes audio files using OpenAI's Whisper model via HuggingFace's Inference API.

## Pre-requisite
Tested on Python 3.12.3

1. Install FFMPEG (for audio processing)
    - For Ubuntu:
    ```bash
    sudo apt install ffmpeg
    ```
    - For other OS, please refer to [FFMPEG Download](https://www.ffmpeg.org/download.html)

2. Ensure application has internet connection

3. Ensure that you have created your HuggingFace API Token, please refer to [Serverless Infernce API](https://huggingface.co/docs/api-inference/en/index)


## Getting Started

### Running Locally

1. Create and activate Python virtual environment
   ```bash
   # Create virtual environment
   python3 -m venv env

   # Activate environment
   source env/bin/activate   # For Linux/Mac
   # or
   .\env\Scripts\activate    # For Windows
   ```
   Note: Requires Python 3.12.3 or above

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables

   Create `/stt/.env` file with the following content:
   ```env
   WHISPER_MODEL=openai/whisper-tiny
   HF_TOKEN=your_hugging_face_api_token_here
   HF_MAX_RETRIES=5
   HF_RETRY_DELAY=2
   ```
   Note: Replace `your_hugging_face_api_token_here` with your actual HuggingFace API token


## Huggingface Resource
- Base model used: [whisper-tiny](https://huggingface.co/openai/whisper-tiny)


## Assumptions
1. No infrastructure to host Whisper model locally, hence using Hugging Face's Inference API

2. Code runs on CPU-only server (no GPU packages installed)

3. Audio content is single channel and not based on dual channel(e.g., Call center recordings, YouTube clips) which might require more preprocessing steps (e.g., downmixing, channel separation)


## Implementation
1. Model Selection:
   - Users can select different Whisper models via `WHISPER_MODEL` environment variable
   - Available models list: [Whisper Models](https://huggingface.co/collections/openai/whisper-release-6501bba2cf999715fd953013)

2. Model Warm-up:
   - FastAPI application sends initial request at startup
   - Prevents cold start issues for first transcription request

3. Audio Processing:
   - Converts uploads to WAV format (uncompressed)
   - Standardizes to single channel
   - Resamples to 16kHz for optimal accuracy

4. Voice Detection:
   - Uses VAD (Voice Activity Detection) to remove silences
   - Improves accuracy and reduces resource usage