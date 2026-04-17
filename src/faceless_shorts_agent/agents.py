from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ShortIdea:
    title: str
    hook: str
    angle: str
    humor_potential: int
    visual_potential: int
    production_ease: int

    @property
    def score(self) -> int:
        return self.humor_potential + self.visual_potential + self.production_ease


def generate_ideas(niche: str, tone: str) -> list[ShortIdea]:
    base = niche.strip().lower()
    return [
        ShortIdea(
            title=f"Why {base} sounds fake but is real",
            hook=f"This {base} fact sounds like someone lost a bet.",
            angle="Use escalating examples that get stranger every few seconds.",
            humor_potential=9,
            visual_potential=8,
            production_ease=9,
        ),
        ShortIdea(
            title=f"The {base} mistake everyone repeats",
            hook=f"Most people explain {base} completely backwards.",
            angle="Set up the common belief, then flip it with a punchy correction.",
            humor_potential=7,
            visual_potential=7,
            production_ease=8,
        ),
        ShortIdea(
            title=f"If {base} had a group chat",
            hook=f"If {base} had a group chat, one message would ruin everything.",
            angle=f"Personify the niche with {tone} dialogue and fast captions.",
            humor_potential=10,
            visual_potential=8,
            production_ease=7,
        ),
        ShortIdea(
            title=f"The tiny detail that changes {base}",
            hook=f"One tiny detail makes {base} way funnier than it should be.",
            angle="Build curiosity around one overlooked detail, then reveal the payoff.",
            humor_potential=8,
            visual_potential=7,
            production_ease=9,
        ),
        ShortIdea(
            title=f"{base.title()} explained badly",
            hook=f"Here is {base} explained in the worst possible way.",
            angle="Use an intentionally silly analogy while still teaching one real thing.",
            humor_potential=9,
            visual_potential=9,
            production_ease=8,
        ),
    ]


def select_best_idea(ideas: list[ShortIdea]) -> ShortIdea:
    return sorted(ideas, key=lambda idea: idea.score, reverse=True)[0]


def write_script(idea: ShortIdea, tone: str, length_seconds: int) -> dict:
    target_words = max(70, min(120, int(length_seconds * 2.4)))
    sentences = [
        idea.hook,
        f"Imagine opening your phone and seeing: '{idea.title}.'",
        "That is the whole vibe.",
        "First, it looks normal.",
        "Then it gets suspicious.",
        "Then it starts making too much sense.",
        f"The trick is this: {idea.angle.lower()}",
        "And just when you think you understand it, the final detail walks in wearing a tiny hat.",
        f"So yes, {idea.title.lower()} is somehow both educational and mildly concerning.",
    ]
    script_parts: list[str] = []
    for sentence in sentences:
        candidate = " ".join([*script_parts, sentence])
        if len(candidate.split()) > target_words and script_parts:
            break
        script_parts.append(sentence)
    script = " ".join(script_parts)
    return {
        "title": idea.title,
        "tone": tone,
        "target_length_seconds": length_seconds,
        "voice_direction": "Playful, quick, clear, lightly sarcastic.",
        "script": script,
    }


def format_srt_time(seconds: float) -> str:
    milliseconds_total = round(seconds * 1000)
    hours = milliseconds_total // 3_600_000
    milliseconds_total %= 3_600_000
    minutes = milliseconds_total // 60_000
    milliseconds_total %= 60_000
    whole_seconds = milliseconds_total // 1000
    milliseconds = milliseconds_total % 1000
    return f"{hours:02d}:{minutes:02d}:{whole_seconds:02d},{milliseconds:03d}"


def make_captions(script: str, target_length_seconds: int) -> str:
    words = re.findall(r"\S+", script)
    if not words:
        return ""

    # Estimate word timing deterministically until real TTS word timestamps are available.
    word_duration = max(0.18, target_length_seconds / len(words))
    lines = []
    for index, word in enumerate(words, start=1):
        start = (index - 1) * word_duration
        end = index * word_duration
        lines.append(str(index))
        lines.append(f"{format_srt_time(start)} --> {format_srt_time(end)}")
        lines.append(word)
        lines.append("")
    return "\n".join(lines)


def make_visual_plan(script: str) -> dict:
    lines = [line.strip() for line in script.split(".") if line.strip()]
    beats = []
    for index, line in enumerate(lines[:8]):
        beats.append(
            {
                "time": f"{index * 4}-{(index + 1) * 4}s",
                "narration": line,
                "visual": f"Fast-cut faceless visual for: {line[:90]}",
                "caption": line[:80],
            }
        )
    return {"format": "1080x1920", "beats": beats}
