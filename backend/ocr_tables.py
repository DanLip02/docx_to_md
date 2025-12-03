from pathlib import Path
import cv2
from paddleocr import PPStructure, save_structure_res

def ocr_table_images(image_paths, output_dir):
    """
    Распознаёт таблицы на картинках с помощью PaddleOCR PPStructure
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    ocr_engine = PPStructure(show_log=False, layout=False)

    all_results = {}

    for img_path in image_paths:
        img = cv2.imread(str(img_path))

        if img is None:
            continue

        # Основной вызов PaddleOCR
        result = ocr_engine(img)

        save_path = output_dir / f"{img_path.stem}.json"
        save_structure_res(save_path, result)

        all_results[str(img_path)] = result

    return all_results
