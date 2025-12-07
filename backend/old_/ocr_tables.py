# backend/ocr_tables.py
import os
from PIL import Image
import numpy as np
from paddleocr import PaddleOCR


ocr = PaddleOCR(
    use_angle_cls=False,
    lang="ru"      # ставь "ru" если нужна кириллица
)


def run_ocr(image: Image.Image):

    img_array = np.array(image)

    raw = ocr.predict(img_array)

    if not raw:
        return []

    blocks = []
    for line in raw[0]:   # PaddleOCR → raw[0] = список распознанных сегментов
        bbox = line[0]    # 4 точки
        text = line[1][0] # строка
        blocks.append({"bbox": bbox, "text": text})

    return blocks


def ocr_blocks_to_markdown(blocks):

    if not blocks:
        return ""

    rows = []

    # Собираем метки (y, x, text)
    for b in blocks:
        x_min = b["bbox"][0][0]
        y_min = b["bbox"][0][1]
        text = b["text"]
        rows.append((y_min, x_min, text))

    # Сортировка по строкам (y), внутри строк — по x
    rows.sort()

    grouped = []
    current = []
    prev_y = None
    threshold = 18  # чувствительность группировки

    for y, x, text in rows:
        if prev_y is None:
            current.append((x, text))
            prev_y = y
            continue

        if abs(y - prev_y) < threshold:
            current.append((x, text))
        else:
            grouped.append(current)
            current = [(x, text)]
        prev_y = y

    if current:
        grouped.append(current)

    # Формируем Markdown
    md_lines = []

    for line in grouped:
        # сортируем внутри строки по x
        line.sort()
        cells = [t for _, t in line]
        md_lines.append("| " + " | ".join(cells) + " |")

    # Если нет строк
    if not md_lines:
        return ""

    # Добавляем разделитель
    num_cols = len(md_lines[0].split("|")) - 2
    separator = "| " + " | ".join("---" for _ in range(num_cols)) + " |"

    md_lines.insert(1, separator)

    return "\n".join(md_lines)


def ocr_image_to_markdown(image_path: str):

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"File not found: {image_path}")

    image = Image.open(image_path).convert("RGB")
    blocks = run_ocr(image)
    md = ocr_blocks_to_markdown(blocks)
    return md


if __name__ == "__main__":
    test_path = r"/images/test_1/media/image3.png"
    md = ocr_image_to_markdown(test_path)

    print("\n===== Markdown Table =====\n")
    print(md)
    print("\n==========================\n")


# # Debug run
# if __name__ == "__main__":
#     ocr = OCRTableExtractor()
#     # md = ocr.extract_markdown_table(
#     #     r"C:\Users\Danch\PycharmProjects\docx_to_md\images\test_1\media\image3.png"
#     # )
#     # print(md)
#
#     pipeline = PaddleOCRVL()
#     output = pipeline.predict(input=r"C:\Users\Danch\PycharmProjects\docx_to_md\images\test_1\media\image3.png")
#     for res in output:
#         res.print()
#         res.save_to_json(save_path="output")
#         res.save_to_markdown(save_path="output")
