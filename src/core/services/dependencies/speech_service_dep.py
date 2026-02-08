from src.core.services.speech_to_text_service import SpeechService

speech_service = SpeechService()


def get_speech_service():
    return speech_service
