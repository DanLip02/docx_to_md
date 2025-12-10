import re
from pathlib import Path
from dataclasses import dataclass
import os

@dataclass
class ImageEntry:
    src: str         # путь из атрибута src
    path: Path       # абсолютный путь
    tag: str         # исходный <img ...> тег целиком

IMG_PATTERN = r'(<img\s+[^>]*src="([^"]+)"[^>]*>)'

def extract_images(md_file_path: str | Path, md_name: str):
    """
    Extract<img ...> from Markdown.

    :param md_file_path: path to  .md falis
    :return: list ImageEntry
    """
    BASE_DIR = Path(__file__).parent.parent
    IMG_DIR = BASE_DIR / "images" / md_name / "media"

    md_path = Path(md_file_path)
    text = md_path.read_text(encoding="utf-8")

    matches = re.findall(IMG_PATTERN, text, flags=re.IGNORECASE)
    results = []

    for tag, src in matches:

        file_name = Path(src).name
        abs_path = IMG_DIR / file_name

        if abs_path.suffix.lower() == ".emf":
            from conver_emf_png import emf_to_png  # твоя функция
            png_path = Path(emf_to_png(str(abs_path), IMG_DIR))
            os.remove(abs_path)
            src = png_path.name
            text = text.replace(file_name, src)

        results.append(
            ImageEntry(
                src=src,
                path=(IMG_DIR / src).resolve(),
                tag=tag
            )
        )

    md_path.write_text(text, encoding="utf-8")
    return results, IMG_DIR



if __name__ == "__main__":
    import os
    working_dir = Path(r"C:\Users\Danch\PycharmProjects\docx_to_md")
    os.chdir(working_dir)

    out = extract_images("output_md/output.md")
    # for img in out:
    #     print("TAG:", img.tag)
    #     print("SRC:", img.src)
    #     print("ABS:", img.path)
    #     print("---")