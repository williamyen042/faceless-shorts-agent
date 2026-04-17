from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .agents import generate_ideas, make_captions, make_visual_plan, select_best_idea, write_script
from .env import load_env_file
from .tts import generate_elevenlabs_voiceover


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a basic faceless Shorts package.")
    parser.add_argument("--niche", required=True, help="The niche/topic for the Short.")
    parser.add_argument("--tone", default="funny and fast-paced", help="Voice and comedy style.")
    parser.add_argument("--length", type=int, default=35, help="Target length in seconds.")
    parser.add_argument("--tts", choices=["none", "elevenlabs"], default="none", help="Optional TTS provider.")
    parser.add_argument("--output-dir", default="output", help="Base output directory.")
    return parser.parse_args()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def make_run_dir(base_dir: str, niche: str) -> Path:
    slug = "".join(char if char.isalnum() else "-" for char in niche.lower()).strip("-")
    slug = "-".join(part for part in slug.split("-") if part)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(base_dir) / f"{timestamp}-{slug[:40]}"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def run_pipeline(args: argparse.Namespace) -> Path:
    load_env_file()
    run_dir = make_run_dir(args.output_dir, args.niche)

    ideas = generate_ideas(args.niche, args.tone)
    selected_idea = select_best_idea(ideas)
    script = write_script(selected_idea, args.tone, args.length)
    captions = make_captions(script["script"], args.length)
    visual_plan = make_visual_plan(script["script"])

    write_json(run_dir / "ideas.json", [asdict(idea) | {"score": idea.score} for idea in ideas])
    write_json(run_dir / "selected_idea.json", asdict(selected_idea) | {"score": selected_idea.score})
    write_json(run_dir / "script.json", script)
    (run_dir / "captions.srt").write_text(captions, encoding="utf-8")
    write_json(run_dir / "visual_plan.json", visual_plan)

    if args.tts == "elevenlabs":
        audio_path = run_dir / "voiceover.mp3"
        metadata = generate_elevenlabs_voiceover(script["script"], audio_path)
        write_json(run_dir / "tts_metadata.json", metadata)

    return run_dir


def main() -> None:
    args = parse_args()
    run_dir = run_pipeline(args)
    print(f"Created Shorts package: {run_dir}")


if __name__ == "__main__":
    main()
