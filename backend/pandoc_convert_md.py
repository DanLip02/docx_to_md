# pandoc_convert_md.py
import subprocess
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent
MD_DIR = BASE_DIR / "output_md"

def convert_docx_md(path):
    """
    basic convertation DOCX → Markdown using Pandoc.
    download media to BASE_DIR/images.
    """

    # path = Path(path)
    file = path
    path = BASE_DIR / "data" / path
    print(path)
    # folders
    if not os.path.exists(path):
        print("File was not found:", path)
        return None

    MD_DIR.mkdir(parents=True, exist_ok=True)

    MEDIA_DIR = BASE_DIR / "images" / f"{file.split('.')[0]}"
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    # final file
    output_md = MD_DIR / f"{path.stem}.md"

    command = [
        "pandoc",
        str(path),
        "-t", "gfm",
        "-o", str(output_md),
        f"--extract-media={MEDIA_DIR}"
    ]

    print("Running:", command)

    subprocess.run(command, check=True)

    return output_md
