import pytesseract
from PIL import Image

image = Image.open(r"/images/test_1/media/image3.png")
data = pytesseract.image_to_data(image, lang='rus', output_type=pytesseract.Output.DICT)

rows = {}
for i, text in enumerate(data['text']):
    if text.strip():
        y = data['top'][i]
        rows.setdefault(y, []).append(text)

for row_y in sorted(rows.keys()):
    row = rows[row_y]
    print("| " + " | ".join(row) + " |")
