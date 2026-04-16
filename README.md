# faceless-shorts-agent

A very small local pipeline for generating a faceless YouTube Shorts package from a niche prompt.

The first version keeps things intentionally simple:

- generates niche-based ideas
- scores and selects one idea
- writes a short script
- creates captions
- creates a visual beat sheet
- optionally generates an ElevenLabs voiceover

No scraping, video assembly, or auto-upload yet.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run the local starter pipeline:

```bash
python src/main.py --niche "weird history facts" --tone "funny and fast-paced" --length 35
```

Outputs are written to a timestamped folder under `output/`.

## ElevenLabs voiceover

Voiceover generation is skipped unless `--tts elevenlabs` is passed and `ELEVENLABS_API_KEY` is set.

```bash
python src/main.py --niche "weird history facts" --tts elevenlabs
```

The default voice ID is Adam:

```text
pNInz6obpgDQGcFmaJgB
```

## Next steps

- Replace the starter idea/script logic with OpenAI API calls.
- Add trend research from selected sources.
- Add video assembly with FFmpeg, MoviePy, or Remotion.
- Add a human approval step before posting.
