import os
import re
import unicodedata
import csv
import shutil

INPUT_OUTPUT_MAP = {
    "imagens": "renomeadas",
    "Pandora": os.path.join("saida", "pandora"),
}

for out in set(INPUT_OUTPUT_MAP.values()):
    os.makedirs(out, exist_ok=True)


def sanitize_filename(filename):
    normalized = unicodedata.normalize('NFKD', filename)
    without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    replaced = without_accents.replace(' ', '_').replace('-', '_')
    sanitized = re.sub(r'[^a-zA-Z0-9_.]', '_', replaced)
    sanitized = re.sub(r'_+', '_', sanitized)  
    return sanitized


def unique_destination(output_dir, filename):
    base, ext = os.path.splitext(filename)
    candidate = filename
    counter = 1
    while os.path.exists(os.path.join(output_dir, candidate)):
        candidate = f"{base}_{counter}{ext}"
        counter += 1
    return candidate


def process_root(input_root, output_base):
    pdf_exts = {'.pdf'}
    archive_exts = {'.zip', '.rar', '.7z', '.tar', '.gz', '.tgz', '.tar.gz'}
    valid_extensions = pdf_exts | archive_exts

    total_files = 0
    processed_files = 0
    report_data = []

    if not os.path.isdir(input_root):
        print(f"Pasta de entrada não encontrada: {input_root} (pulando)")
        return

    for root, _, files in os.walk(input_root):
        for filename in files:
            total_files += 1
            input_path = os.path.join(root, filename)
            lower = filename.lower()
            if any(lower.endswith(ext) for ext in valid_extensions):
                relative_path = os.path.relpath(root, input_root)
                if relative_path == '.':
                    relative_path = ''
                output_dir = os.path.join(output_base, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                try:
                    name_part, ext = os.path.splitext(filename)
                    new_name_part = sanitize_filename(name_part)
                    ext = ext.lower()
                    new_filename = new_name_part + ext
                    new_filename = unique_destination(output_dir, new_filename)
                    output_path = os.path.join(output_dir, new_filename)
                    shutil.copy2(input_path, output_path)
                    processed_files += 1
                    report_data.append([input_path, output_path, "Success"])
                    print(f"Renomeado: {input_path} -> {output_path}")
                except Exception as e:
                    report_data.append([input_path, "", f"Error: {e}"])
                    print(f"Erro ao processar {input_path}: {e}")
            else:
                report_data.append([input_path, "", "Skipped: Invalid file type"])

    report_path = os.path.join(output_base, "conversion_report.csv")
    try:
        with open(report_path, mode='w', newline='', encoding='utf-8') as report_file:
            writer = csv.writer(report_file)
            writer.writerow(["Original Path", "New Path", "Status"])
            writer.writerows(report_data)
        print(f"Relatório gerado em: {report_path}")
    except Exception as e:
        print(f"Falha ao escrever relatório {report_path}: {e}")

    print(f"[{input_root}] Total de arquivos: {total_files}")
    print(f"[{input_root}] Arquivos processados: {processed_files}")


def rename_images_and_pandora():
    for input_root, output_base in INPUT_OUTPUT_MAP.items():
        process_root(input_root, output_base)


if __name__ == "__main__":
    rename_images_and_pandora()
