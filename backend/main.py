# from pipeline import run_pipeline
from extract_images import *
import os
from pathlib import Path
from upd_md import *
from pandoc_convert_md import convert_docx_md
from classify_images import *
import json

def replace_image_with_markdown(md_path: str, image_name: str, md_content: str):
    """
    Заменяет тег картинки в .md на сгенерированный Markdown-блок.
    """

    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Тег может быть (![...](img.png)) или прямой <img>
    patterns = [
        fr"!\[[^\]]*\]\({image_name}\)",
        fr"<img[^>]*{image_name}[^>]*>"
    ]

    import re
    for p in patterns:
        text = re.sub(p, md_content, text)

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(text)

if __name__ == "__main__":

    BASE_DIR = Path(__file__).parent.parent

    file_ = "test_1.docx"
    input_file = Path(f"data/{file_}")
    output_md = convert_docx_md(file_)
    print("Ready! Markdown saved into:", output_md)


    print(output_md)
    images, image_paths = extract_images(output_md, file_.split(".")[0])
    print("Images found:", images)


    out = classify_all_images(image_paths)

    classification_path = BASE_DIR / "classification_json" / f"result_{file_.split(".")[0]}.json"

    with open(classification_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=4, ensure_ascii=False)

    with open(classification_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = {}

    for filename, info in data.items():
        label = info.get("label")
        img_path = info.get("path")

        if not img_path or not os.path.exists(img_path):
            print(f"[WARN] File {img_path} was not found.")
            continue

        print(f"Now is working: {filename}")

        try:
            if label == "image":
                md_text = extract_image_md(img_path)
            elif label == "table":
                md_text = extract_table_md(img_path)
            else:
                print(f"[WARN] strange lebel'{label}' for file {filename}")
                md_text = None
        except Exception as e:
            print(f"[ERROR] error preprocessing {filename}: {e}")
            md_text = None


        results[filename] = {
            "label": label,
            "path": img_path,
            "md": md_text or "-"
        }

    # MD_DIR = BASE_DIR / "output_md" / file_.split(".")[0]
    output_path = replace_images_in_md(output_md, results)
    print(f"Done! Result saved in {output_path}")
