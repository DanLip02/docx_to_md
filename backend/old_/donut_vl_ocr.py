from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
from pathlib import Path

# Загружаем модель и процессор один раз
MODEL_NAME = "naver-clova-ix/donut-base"
processor = DonutProcessor.from_pretrained(MODEL_NAME)
model = VisionEncoderDecoderModel.from_pretrained(MODEL_NAME)

def convert_image_to_md(image_path: str | Path) -> Path:
    image_path = Path(image_path)
    image = Image.open(image_path).convert("RGB")

    # Префикс для генерации текста документа
    prompt = "<s_doc>"

    pixel_values = processor(image, return_tensors="pt").pixel_values

    outputs = model.generate(
        pixel_values,
        decoder_input_ids=processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt").input_ids,
        max_length=1024
    )

    text = processor.batch_decode(outputs, skip_special_tokens=True)[0]

    # Сохраняем в Markdown
    md_path = image_path.with_suffix(".md")
    md_path.write_text(text, encoding="utf-8")

    print(f"[INFO] Markdown создан: {md_path}")
    return md_path

# Пример вызова
if __name__ == "__main__":
    convert_image_to_md(r"/images/test_1/media/image3.png")
