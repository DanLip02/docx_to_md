from paddleocr import PaddleOCRVL
pipeline = PaddleOCRVL()
output = pipeline.predict(r"C:\Users\Danch\PycharmProjects\docx_to_md\images\test_1\media\image3.png")
for res in output:
    res.print()
    res.save_to_json(save_path="classification_json")
    res.save_to_markdown(save_path="output_md")