"""Generate Agent Atelier's original cozy-jazz WAV track."""

from __future__ import annotations

import math
import random
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 22_050
DURATION = 40.0
SEGMENT = 8.0
OUTPUT = Path(__file__).resolve().parents[1] / "assets" / "audio" / "agent-atelier-ambient.wav"

# Cmaj7 → Am7 → Dm7 → G9 → Cmaj7: a calm, familiar jazz turnaround.
CHORDS = (
    (130.81, 164.81, 196.00, 246.94),
    (110.00, 130.81, 164.81, 196.00),
    (146.83, 174.61, 220.00, 261.63),
    (98.00, 123.47, 146.83, 174.61, 220.00),
    (130.81, 164.81, 196.00, 246.94),
)


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def electric_piano(age: float, frequency: float) -> float:
    """A soft Rhodes-like note with no samples or external recordings."""
    if age < 0.0 or age > 3.2:
        return 0.0
    attack = smoothstep(age / 0.045)
    decay = math.exp(-1.22 * age)
    phase = 2.0 * math.pi * frequency * age
    tone = (
        math.sin(phase)
        + 0.22 * math.sin(phase * 2.0 + 0.18)
        + 0.07 * math.sin(phase * 3.0)
    )
    return tone * attack * decay


def chord_pad(time: float, chord: tuple[float, ...], start: float) -> float:
    local = time - start
    if local < -1.0 or local > SEGMENT + 1.0:
        return 0.0
    fade_in = smoothstep((local + 0.9) / 1.7)
    fade_out = smoothstep((SEGMENT + 0.9 - local) / 1.7)
    envelope = min(fade_in, fade_out)
    if envelope <= 0.0:
        return 0.0
    gentle_pulse = 0.93 + 0.07 * math.sin(2.0 * math.pi * 0.125 * max(local, 0.0))
    voices = 0.0
    for index, frequency in enumerate(chord):
        phase = 2.0 * math.pi * frequency * time
        voices += math.sin(phase) * (0.034 if index == 0 else 0.022)
    return voices * envelope * gentle_pulse


def melody(time: float) -> float:
    value = 0.0
    for segment_index, chord in enumerate(CHORDS):
        start = segment_index * SEGMENT
        # Sparse one-note-at-a-time voicings leave room for the tutorial UI.
        pattern = (0, 2, 1, min(3, len(chord) - 1))
        for offset, note_index in zip((0.5, 2.5, 4.5, 6.5), pattern):
            value += electric_piano(time - start - offset, chord[note_index] * 2.0) * 0.055
    return value


def sample(time: float, soft_noise: float) -> float:
    pad = 0.0
    for index, chord in enumerate(CHORDS):
        pad += chord_pad(time, chord, index * SEGMENT)
    bass_index = min(len(CHORDS) - 1, int(time / SEGMENT))
    bass_frequency = CHORDS[bass_index][0] / 2.0
    bass = math.sin(2.0 * math.pi * bass_frequency * time) * 0.035
    master_fade = min(smoothstep(time / 1.2), smoothstep((DURATION - time) / 1.2))
    return (pad + bass + melody(time) + soft_noise * 0.0025) * master_fade


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    random_source = random.Random(3712)
    filtered_noise = 0.0
    frames = bytearray()
    for frame in range(int(SAMPLE_RATE * DURATION)):
        time = frame / SAMPLE_RATE
        white = random_source.uniform(-1.0, 1.0)
        filtered_noise = filtered_noise * 0.995 + white * 0.005
        value = max(-1.0, min(1.0, sample(time, filtered_noise)))
        frames.extend(struct.pack("<h", round(value * 32_767)))

    with wave.open(str(OUTPUT), "wb") as destination:
        destination.setnchannels(1)
        destination.setsampwidth(2)
        destination.setframerate(SAMPLE_RATE)
        destination.writeframes(frames)

    print(f"Generated cozy-jazz track: {OUTPUT} ({OUTPUT.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
