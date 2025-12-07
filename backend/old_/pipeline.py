from backend.old_.extract_tables import extract_tables
from ocr_tables import ocr_table_images
import json
from extract_images import *


def print_tables_md(tables):
    """
    Печатает список таблиц в формате Markdown
    """
    print("\n=== Таблицы в Markdown ===\n")

    for idx, table in enumerate(tables, start=1):
        print(f"### Таблица {idx}\n")

        if not table:
            print("_Пустая таблица_\n")
            continue

        header = table[0]
        cols = len(header)

        print("| " + " | ".join(header) + " |")
        print("|" + " | ".join(["---"] * cols) + "|")

        for row in table[1:]:
            print("| " + " | ".join(row) + " |")

        print("\n")


def run_pipeline(
    docx_path: str,
    tmp_dir: str = "tmp",
    print_md: bool = True,
    enable_ocr: bool = True,
):
    """
    Полный пайплайн обработки DOCX:
    1. Извлекает нативные таблицы python-docx
    2. Извлекает картинки из DOCX
    3. Прогоняет OCR для извлечения таблиц из картинок (если включено)
    4. Сохраняет результаты в JSON
    5. Опционально печатает в Markdown

    Parameters
    ----------
    docx_path : str
    tmp_dir : str
    print_md : bool
        Печатать ли таблицы в Markdown
    enable_ocr : bool
        Включать ли OCR-обработку изображений
    """

    docx_path = Path(docx_path)
    tmp_dir = Path(tmp_dir)
    tmp_dir.mkdir(exist_ok=True)

    native_tables = extract_tables(docx_path)

    native_file = tmp_dir / f"{docx_path.stem}_native_tables.json"
    native_file.write_text(
        json.dumps(native_tables, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    if print_md:
        print("### Нативные таблицы (python-docx)\n")
        print_tables_md(native_tables)

    img_dir = tmp_dir / "images"
    img_dir.mkdir(exist_ok=True)

    image_paths = extract_images(docx_path, img_dir)
    ocr_tables = {}

    if enable_ocr and image_paths:
        ocr_dir = tmp_dir / "ocr"
        ocr_dir.mkdir(exist_ok=True)

        ocr_tables = ocr_table_images(image_paths, ocr_dir)

        ocr_file = tmp_dir / f"{docx_path.stem}_ocr_tables.json"
        ocr_file.write_text(
            json.dumps(ocr_tables, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        if print_md and ocr_tables:
            print("\n### Таблицы, полученные через OCR\n")
            for img, parsed in ocr_tables.items():
                print(f"\n**Источник: {img}**\n")
                # parsed — это структура PaddleOCR, её нужно нормализовать
                # но пока просто печатаем raw или сами скажете как форматировать
                print(f"`{json.dumps(parsed, ensure_ascii=False)}`\n")

    print(
        f"\nГОТОВО: извлечено "
        f"{len(native_tables)} нативных таблиц, "
        f"{len(image_paths)} изображений, "
        f"{len(ocr_tables)} OCR-таблиц."
    )

    return {
        "native": native_tables,
        "images": [str(x) for x in image_paths],
        "ocr": ocr_tables,
    }
