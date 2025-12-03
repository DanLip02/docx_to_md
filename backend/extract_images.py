
import re
from pathlib import Path
from dataclasses import dataclass

@dataclass
class ImageEntry:
    src: str         # путь из атрибута src
    path: Path       # абсолютный путь
    tag: str         # исходный <img ...> тег целиком

IMG_PATTERN = r'(<img\s+[^>]*src="([^"]+)"[^>]*>)'

def extract_images(md_file_path: str | Path):
    """
    Извлекает все <img ...> из Markdown-файла.

    :param md_file_path: путь к .md файлу
    :return: список ImageEntry
    """
    md_path = Path(md_file_path)
    text = md_path.read_text(encoding="utf-8")

    # Директория с изображениями
    img_dir = Path("images/media").resolve()

    matches = re.findall(IMG_PATTERN, text, flags=re.IGNORECASE)
    results = []

    for tag, src in matches:
        # Берём только имя файла, чтобы не дублировать директории
        file_name = Path(src).name
        abs_path = (img_dir / file_name).resolve()

        # Проверяем EMF
        if abs_path.suffix.lower() == ".emf":
            from conver_emf_png import emf_to_png  # твоя функция
            png_path = Path(emf_to_png(abs_path, img_dir))
            os.remove(abs_path)
            src = png_path.name
            text = text.replace(file_name, src)

        results.append(
            ImageEntry(
                src=src,
                path=(img_dir / src).resolve(),
                tag=tag
            )
        )

    # Сохраняем MD с обновлёнными путями
    md_path.write_text(text, encoding="utf-8")
    return results

    # Сохраняем MD с обновлёнными путями
    md_path.write_text(text, encoding="utf-8")
    return results


if __name__ == "__main__":
    import os
    working_dir = Path(r"C:\Users\Danch\PycharmProjects\docx_to_md")
    os.chdir(working_dir)  # смена текущей директории

    out = extract_images("output_md/output.md")
    # for img in out:
    #     print("TAG:", img.tag)
    #     print("SRC:", img.src)
    #     print("ABS:", img.path)
    #     print("---")