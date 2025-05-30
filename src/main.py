import sys
import asyncio

import edge_tts


CONFIG: dict[str, str | tuple[str, str, str]] = {
    "language_islands_path": "src/language-islands",
    "outputs_path": "src/outputs/english",
    "puntuation_symbols": (".", "?", "!"),
    "tts_voice": "en-US-AndrewNeural",
}


def get_filename() -> str:
    if len(sys.argv) != 2:
        print(f"[ERROR]: Usage python {sys.argv[0]} <language-island-filename>")
        sys.exit(1)

    return sys.argv[1]


def get_raw_sentences(filename: str) -> list[str]:
    with open(f"{CONFIG['language_islands_path']}/{filename}") as language_islands:
        raw_sentences: list[str] = []
        raw_sentences = language_islands.read().split("\n")
        raw_sentences = list(
            filter(lambda sentence: len(sentence.strip()) > 0, raw_sentences)
        )

        return raw_sentences


def verify_sentence(sentence: str) -> str:
    verified_sentence = sentence

    verified_sentence = sentence.strip()

    if not verified_sentence.endswith(CONFIG["puntuation_symbols"]):
        verified_sentence += "."

    return verified_sentence


def get_formatted_sentences(sentences: list[str]) -> list[str]:
    formatted_sentences: list[str] = []
    for sentence in sentences:
        verified_sentence = verify_sentence(sentence) + "\n"

        for _ in range(5):
            formatted_sentences.append(verified_sentence)

    return formatted_sentences


def format_tts_text(sentences: list[str]) -> str:
    return "".join(sentences)


def save_exercise(filename: str, content: str) -> None:
    exercise_path = f"{CONFIG["outputs_path"]}/{filename}"
    with open(exercise_path, "w") as file:
        file.write(str(content))


def get_tts_text(filename: str) -> str:
    raw_sentences = get_raw_sentences(filename)
    formatted_sentences = get_formatted_sentences(raw_sentences)

    tts_text = format_tts_text(formatted_sentences)

    save_exercise(filename, tts_text)

    return tts_text


async def amain() -> None:
    """Main function"""

    filename_with_ext = get_filename()
    filename = filename_with_ext.split(".").pop(0)
    tts_text = get_tts_text(filename_with_ext)

    communicate = edge_tts.Communicate(tts_text, str(CONFIG["tts_voice"]))
    await communicate.save(f"{CONFIG["outputs_path"]}/{filename}.mp3")


if __name__ == "__main__":
    asyncio.run(amain())
