# image_to_md.py
from rapidocr import RapidOCR
from typing import List, Dict
import numpy as np

ocr = RapidOCR()  # инициализация OCR (CPU или GPU)


def convert_image_to_md(image_path: str) -> str:
    result = ocr(image_path)
    boxes = result.boxes
    texts = result.txts

    if not texts:
        return ""

    # Сортируем блоки по верхней координате y
    y_coords = [b[:,1].min() for b in boxes]
    sorted_indices = np.argsort(y_coords)
    sorted_boxes = boxes[sorted_indices]
    sorted_texts = [texts[i] for i in sorted_indices]

    lines = []
    current_line = []
    current_y = None
    threshold = 10  # порог по вертикали для определения одной линии

    for b, t in zip(sorted_boxes, sorted_texts):
        top_y = b[:,1].min()
        if current_y is None:
            current_y = top_y
            current_line.append((b[:,0].min(), t))  # x и текст
        elif abs(top_y - current_y) < threshold:
            current_line.append((b[:,0].min(), t))
        else:
            # сортировка по x внутри линии
            current_line.sort(key=lambda x: x[0])
            line_text = " ".join([x[1] for x in current_line])
            lines.append(line_text + "  ")  # двойной пробел = перенос в Markdown
            current_line = [(b[:,0].min(), t)]
            current_y = top_y

    # последняя линия
    if current_line:
        current_line.sort(key=lambda x: x[0])
        line_text = " ".join([x[1] for x in current_line])
        lines.append(line_text + "  ")

    return "\n".join(lines)

# Пример использования:
if __name__ == "__main__":
    md_text = convert_image_to_md(r"/images/test_1/media/image3.png")
    with open("output.md", "w", encoding="utf-8") as f:
        f.write(md_text)
    print("Markdown saved to output.md")
