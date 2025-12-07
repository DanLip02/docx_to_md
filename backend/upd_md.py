import re
from pathlib import Path

def replace_images_in_md(md_path: str | Path, results: dict) -> Path:
    md_path = Path(md_path)

    text = md_path.read_text(encoding="utf-8")

    img_tag_pattern = re.compile(
        r'<img\s+[^>]*src="([^"]+)"[^>]*\/?>',
        flags=re.IGNORECASE
    )
    for match in img_tag_pattern.finditer(text):
        full_tag = match.group(0)
        img_src = match.group(1)

        filename = Path(img_src).name

        if filename not in results:

            continue

        replacement_md = results[filename]["md"]

        text = text.replace(full_tag, replacement_md)

    output_path = md_path.with_name(md_path.stem + "_replaced.md")
    output_path.write_text(text, encoding="utf-8")

    return output_path