from abc import ABC, abstractmethod


class Transcriber(ABC):
    @abstractmethod
    def transcribe(self, audio_path: str) -> str: ...


class OpenAITranscriber(Transcriber):
    def __init__(self, api_key: str = "", model: str = "whisper-1"):
        import os

        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.model = model

    def transcribe(self, audio_path: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.api_key)
        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(model=self.model, file=f)
        return result.text


class FasterWhisperTranscriber(Transcriber):
    def __init__(self, model: str = "base.en"):
        self.model_name = model
        self._model = None

    @property
    def model(self):
        if self._model is None:
            from faster_whisper import WhisperModel

            self._model = WhisperModel(self.model_name, compute_type="int8")
        return self._model

    def transcribe(self, audio_path: str) -> str:
        segments, _ = self.model.transcribe(audio_path)
        return " ".join(seg.text for seg in segments).strip()


def get_transcriber(config: dict) -> Transcriber:
    backend = config.get("backend", "openai")
    model = config.get("model", "")

    if backend == "openai":
        return OpenAITranscriber(
            api_key=config.get("openai_api_key", ""),
            model=model or "whisper-1",
        )
    elif backend == "faster-whisper":
        return FasterWhisperTranscriber(model=model or "base.en")
    else:
        raise ValueError(f"Unknown STT backend: {backend}")
