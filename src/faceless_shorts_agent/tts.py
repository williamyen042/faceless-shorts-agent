from __future__ import annotations

import os
from pathlib import Path


ADAM_VOICE_ID = "pNInz6obpgDQGcFmaJgB"


def generate_elevenlabs_voiceover(text: str, output_path: Path) -> dict:
    import requests

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required when running with --tts elevenlabs.")

    voice_id = os.getenv("ELEVENLABS_VOICE_ID", ADAM_VOICE_ID)
    model_id = os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2")

    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
        headers={
            "xi-api-key": api_key,
            "Content-Type": "application/json",
        },
        params={"output_format": "mp3_44100_128"},
        json={
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.45,
                "similarity_boost": 0.85,
                "style": 0.35,
                "use_speaker_boost": True,
            },
        },
        timeout=60,
    )
    response.raise_for_status()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(response.content)

    return {
        "provider": "elevenlabs",
        "voice_id": voice_id,
        "model_id": model_id,
        "output_path": str(output_path),
        "script_length_chars": len(text),
    }
