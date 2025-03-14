import logging
from faster_whisper import WhisperModel
from config import WHISPER_MODEL, WHISPER_DEVICE, WHISPER_COMPUTE_TYPE

logger = logging.getLogger(__name__)

# Initialize Whisper model
model = None

def init_whisper():
    """Initialize the Whisper model."""
    global model
    model = WhisperModel(WHISPER_MODEL, device=WHISPER_DEVICE, compute_type=WHISPER_COMPUTE_TYPE)
    logger.info(f"Whisper model '{WHISPER_MODEL}' initialized")
    return model

def get_model():
    """Get the Whisper model, initializing it if necessary."""
    global model
    if model is None:
        model = init_whisper()
    return model

def transcribe_audio(file_path):
    """Transcribe an audio file using Whisper."""
    model = get_model()
    
    logger.info(f"Transcribing audio file: {file_path}")
    segments, info = model.transcribe(str(file_path))
    
    # Combine all segments into a single transcription
    transcription = " ".join([segment.text for segment in segments])
    
    logger.info(f"Transcription completed, length: {len(transcription)} characters")
    return transcription 