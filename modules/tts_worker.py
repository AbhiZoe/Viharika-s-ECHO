"""Lightweight TTS subprocess – reads lines from stdin, speaks them, writes DONE."""
import sys

import pyttsx3


def main() -> None:
    rate = int(sys.argv[1]) if len(sys.argv) > 1 else 175
    engine = pyttsx3.init()
    engine.setProperty("rate", rate)

    # Pick a female voice
    voices = engine.getProperty("voices")
    for v in voices:
        name = v.name.lower()
        if "female" in name or "zira" in name or "hazel" in name:
            engine.setProperty("voice", v.id)
            break
    else:
        if len(voices) > 1:
            engine.setProperty("voice", voices[1].id)

    sys.stdout.write("READY\n")
    sys.stdout.flush()

    for line in sys.stdin:
        text = line.strip()
        if text:
            engine.say(text)
            engine.runAndWait()
            sys.stdout.write("DONE\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
