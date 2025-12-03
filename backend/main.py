# from pipeline import run_pipeline
from extract_images import *
import os

if __name__ == "__main__":
    # tables, images = run_pipeline("/Users/danilalipatov/PycharmProjects/docx_ot_md/data/Доклад на РК_РДВ_ноя 25.docx")
    working_dir = Path(r"C:\Users\Danch\PycharmProjects\docx_to_md")
    os.chdir(working_dir)  # смена текущей директории

    out = extract_images("output_md/output.md")

    for obj in out:
        print(obj.src)
