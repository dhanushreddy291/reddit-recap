from pathlib import Path

import edge_tts


def generate_audio_from_text(text: str, output_file: str):
    communicate = edge_tts.Communicate(text, "en-GB-SoniaNeural")
    communicate.save_sync(output_file)


if __name__ == "__main__":
    cwd = Path(__file__).resolve().parent
    with open(f"{cwd}/mock_data/reddit_news_summary.txt") as f:
        text = f.read()
    file_path_to_save = f"{cwd}/mock_data/reddit_news_summary.mp3"
    generate_audio_from_text(text, file_path_to_save)
