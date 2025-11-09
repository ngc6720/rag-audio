import json
import requests
from typing import Annotated
from ....config import Config
from ..models import ITranscriber, Transcript


class TranscriberApi(ITranscriber):
    def get_transcription_from_file(
        self,
        file_name: str,
        file: bytes,
    ):
        url = "https://api.mistral.ai/v1/audio/transcriptions"
        headers = {
            "Authorization": f"Bearer {Config().secrets.mistral_api_key}",
        }

        files = {"file": ("conversation_sesameai.wav", file)}
        data = {
            "model": "voxtral-mini-latest",
            "timestamp_granularities": ["segment"],
        }
        response = requests.post(url, files=files, data=data, headers=headers)
        return Transcript.model_validate(response.json())


class TranscriberMock(ITranscriber):
    def get_transcription_from_file(
        self,
        file_name: str,
        file: bytes,
    ):
        with open(f"{Config().ROOT_PATH}/test_media/transcript.json") as f:
            result = json.load(f)["transcription"]
            return Transcript.model_validate(result)
