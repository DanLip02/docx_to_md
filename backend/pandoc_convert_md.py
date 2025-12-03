import subprocess
from pathlib import Path
import os


working_dir = Path(r"C:\Users\Danch\PycharmProjects\docx_to_md")
os.chdir(working_dir)  # смена текущей директории


# Пути
# input_file = Path(r"data\Доклад_на_РК_РДВ_ноя_25.docx")
# output_file = Path(r"output_md\output.md")
# media_dir = Path(r"images")
input_file = Path("data/test_1.docx")
output_file = Path("output_md/output.md")
media_dir = Path("images")
# Создаём папку для медиа, если её нет
output_file.parent.mkdir(parents=True, exist_ok=True)
media_dir.mkdir(parents=True, exist_ok=True)

# command Pandoc
"""
command = [
    "pandoc",
    str(input_file),
    "-t", "markdown",
    "-o", str(output_file),
    f"--extract-media={media_dir}"
]
"""
command = [
    "pandoc",
    str(input_file),
    "-t", "gfm",
    "-o", str(output_file),
    f"--extract-media={media_dir}"
]
print(command)
# Запуск
subprocess.run(command, check=True)
