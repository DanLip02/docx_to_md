import subprocess
import os
from pathlib import Path

def emf_to_png(emf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if not os.path.exists(emf_path):
        print("File was not found:", emf_path)
        return None
    else:
        base_name = os.path.splitext(os.path.basename(emf_path))[0]
        png_path = os.path.join(output_dir, base_name + ".png")
        subprocess.run(["magick", "-density", "300", emf_path, png_path], check=True)
        return png_path


if __name__ =='__main__':

    BASE_DIR = Path(__file__).parent.parent

    MD_DIR = BASE_DIR / "output_md"
    IMG_DIR = BASE_DIR / "images/media"

    md_file = str(MD_DIR / "output.md")
    png_path = str(IMG_DIR / "image5.emf")
    png_file = emf_to_png(png_path, IMG_DIR)
    print("Создан PNG:", png_file)
