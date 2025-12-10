from extract_images import *
from upd_md import *
from pandoc_convert_md import convert_docx_md
from classify_images import extract_image_md, extract_table_md, classify_all_images
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import shutil
import uvicorn


app = FastAPI(title="LLM Pipeline API")


@app.post("/process")
async def process_file(file: UploadFile = File(...)):

    BASE_DIR = Path(__file__).parent.parent
    print(Path(__file__).parent.parent)
    UPLOAD_DIR = BASE_DIR / "data"

    if not file:
        raise HTTPException(status_code=400, detail="Файл не передан")

    print(file.filename)
    file_path = UPLOAD_DIR / file.filename

    print(file_path)
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    print(file_path)
    try:
        result = run_main(file.filename)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    return JSONResponse(content={"result": result})

def run_main(file_: str | Path):
    BASE_DIR = Path(__file__).parent.parent

    output_md = convert_docx_md(file_)
    print("Ready! Markdown saved into:", output_md)

    print(output_md)
    images, image_paths = extract_images(output_md, file_.split(".")[0])
    print("Images found:", images)

    if len(images) > 0:
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

        output_path = replace_images_in_md(output_md, results)
        return f"Done! Result saved in {output_path}"
    else:
        return f"There were not any images, check {output_md}"

if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=5432, reload=True)