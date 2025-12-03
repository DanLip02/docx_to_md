from docx import Document

def extract_tables(docx_path):
    """
    Извлекает все структурные таблицы из DOCX
    Возвращает список таблиц в виде списка списков строк
    """
    doc = Document(docx_path)
    all_tables = []

    for tbl in doc.tables:
        table_data = []
        for row in tbl.rows:
            table_data.append([cell.text.strip() for cell in row.cells])
        all_tables.append(table_data)

    return all_tables
