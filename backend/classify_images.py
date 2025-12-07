import os
import base64
import json
# from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import requests
from typing import List, Optional, Any
from pydantic import BaseModel

load_dotenv()
API_LLM_KEY = os.getenv("API_LLM_KEY")
BASE_URL_LLM = os.getenv("URL_LLM")


# client = OpenAI(base_url=f"{BASE_URL_LLM}/v1/", api_key="YOUR_API_KEY")


class Message(BaseModel):
    role: str
    content: Optional[str] = None
    tool_calls: Optional[List[Any]] = None


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Optional[Any] = None
    finish_reason: Optional[str] = None


class Usage(BaseModel):
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None


class ChatCompletionResponse(BaseModel):
    id: Optional[str]
    object: Optional[str]
    created: Optional[int]
    model: Optional[str]
    choices: List[Choice]
    usage: Optional[Usage] = None
    stats: Optional[dict] = None
    system_fingerprint: Optional[str] = None


def encode_image(path: str) -> str:
    """Reading + convert to base64 (possible to be sent into LLM (QWEN for ex.)"""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def classify_image_llm(image_path: str) -> str:
    """
    Classify using  Vision LLM.
    Return: "table" or "image" + can be returned description.
    """

    img_base64 = encode_image(image_path)

    prompt = """Привет ! 
        Дай классификацию данного изображение - таблица или картинка.
        Учти, что таблица характерезуется в основном линиями и большим колличеством цирф (чисел) - в противном случае может быть изображение. 
        Верни в формате json без дополнительного текста. 
        Формат json имеет вид {'type': '...', 'discription':'...'}, где type - table / image """

    image_url = f"data:image/png;base64,{img_base64}"

    response = requests.post(
        f"{BASE_URL_LLM}/v1/chat/completions",
        headers={"Authorization": f"{API_LLM_KEY}"},
        json={
            "model": os.getenv("MODEL"),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "auto"}}
                    ]
                }
            ]
        }
    )

    parsed = ChatCompletionResponse(**response.json())
    label = json.loads(parsed.choices[0].message.content.strip().lower())["type"]

    # If nothing - error / null (right now used null)
    if label not in ["table", "image"]:
        label = "null"

    return label


def classify_all_images(folder_path: str) -> dict:
    """
    Classify each PNG/JPG images in the folder.
    Return dict.
    """
    results = {}

    for file in os.listdir(folder_path):
        if file.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
            full_path = os.path.join(folder_path, file)
            full_path = os.path.normpath(full_path)
            full_path_unix = full_path.replace("\\", "/")  # for LM Studio

            if not os.path.isfile(full_path):
                print(f"File not found: {full_path}")
                continue

            print(f"Classifying: {file}")
            print(f"path: {full_path_unix}")

            label = classify_image_llm(full_path_unix)
            results[file] = {"label": label, "path": full_path}

    return results

def extract_table_md(image_path: str) -> str:
    """

    """

    image_base64 = encode_image(image_path)

    prompt = """
    Convert the table on the image to HTML.
    
    Rules:
    1. Preserve the exact number of columns and rows.
    2. Keep empty cells as "-".
    3. Do NOT add commentary.
    4. No explanations. Only clean HTML.
    5. Do not merge cells visually – treat each visible cell as a separate cell.
    6. Strictly follow the table structure.
    
    Output: ONLY HTML table. Bit I do not need format for markdown exatcly with specific ``` html ... ```.
    """

    image_url = f"data:image/png;base64,{image_base64}"

    response = requests.post(
        f"{BASE_URL_LLM}/v1/chat/completions",
        headers={"Authorization": f"{API_LLM_KEY}"},
        json={
            "model": os.getenv("MODEL_OCR", os.getenv("MODEL")),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "auto"}}
                    ]
                }
            ],
            "temperature": 0.05,
            "top_p": 0.9,
            "top_k": 10,
            "repetition_penalty": 1,
            "stream": False
        }
    )

    parsed = ChatCompletionResponse(**response.json())
    md = parsed.choices[0].message.content.strip().lower()
    return md.strip()

def extract_image_md(image_path: str) -> str:
    """

    """

    image_base64 = encode_image(image_path)

    prompt = """
    You are converting an image to text description.
    
    Rules:
    1. Describe only what is visible.
    2. No hallucinations.
    3. No extra commentary or reasoning.
    4. Output must be a single text block (text only).
    """

    image_url = f"data:image/png;base64,{image_base64}"

    response = requests.post(
        f"{BASE_URL_LLM}/v1/chat/completions",
        headers={"Authorization": f"{API_LLM_KEY}"},
        json={
            "model": os.getenv("MODEL_OCR", os.getenv("MODEL")),
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_url, "detail": "auto"}}
                    ]
                }
            ],
            "temperature": 0.15,
            "top_p": 0.8,
            "top_k": 2,
            "repetition_penalty": 1.2,
            "stream": False
        }
    )

    parsed = ChatCompletionResponse(**response.json())
    md = parsed.choices[0].message.content.strip().lower()
    return md.strip()

if __name__ == "__main__":
    working_dir = Path(r"C:\Users\Danch\PycharmProjects\docx_to_md")
    os.chdir(working_dir)  # Chanche current directory

    # folder = "images/media"  # path to folder with images
    # out = classify_all_images(folder)
    #
    # with open("classification_result_new.json", "w", encoding="utf-8") as f:
    #     json.dump(out, f, indent=4, ensure_ascii=False)

    print("Done! Result saved in classification_result.json")

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
    stop = 0
    print(results)