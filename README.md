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
- Upgrade word-by-word captions to use real TTS or transcription word timestamps instead of estimated timing.
- Add trend research from selected sources.
- Add video assembly with FFmpeg, MoviePy, or Remotion.
- Add a human approval step before posting.

## Workflow

The starter workflow lives at `workflows/shorts_mvp.json`.

It defines which agent owns each step:

1. `idea_generator` creates video ideas.
2. `idea_scorer` picks the strongest idea.
3. `script_writer` drafts the narration.
4. `script_editor` tightens the script.
5. `caption_builder` creates captions.
6. `visual_planner` creates scene beats and asset ideas.
7. `tts_generator` optionally creates the voiceover.

Each agent has a matching prompt in `prompts/` when it needs model instructions.
