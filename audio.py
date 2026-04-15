import whisper
import warnings
from config import WHISPER_MODEL

warnings.filterwarnings("ignore")

class AudioProcessor:
    def __init__(self):
        #Loading the model
        print(f"Loading Whisper '{WHISPER_MODEL}' model. This might take a sec...")
        self.model = whisper.load_model(WHISPER_MODEL)

    def process(self, file_path: str) -> str:
        print(f"Transcribing: {file_path}")
        try:
            res = self.model.transcribe(file_path)
            return res.get("text", "").strip()
        except Exception as e:
            print(f"Transcription failed: {e}")
            return ""