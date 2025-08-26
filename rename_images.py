import os
import re
import unicodedata
import csv

input_folder = "imagens"
output_folder = "renomeadas"

os.makedirs(output_folder, exist_ok=True)

def sanitize_filename(filename):
    normalized = unicodedata.normalize('NFKD', filename)
    without_accents = ''.join(c for c in normalized if not unicodedata.combining(c))
    without_hyphens = without_accents.replace('-', '_')
    sanitized = re.sub(r'[^a-zA-Z0-9_.-]', '_', without_hyphens)
    sanitized = re.sub(r'_+', '_', sanitized)  # Replace multiple underscores
    return sanitized

def rename_images():
    valid_extensions = {'.jpg', '.jpeg', '.tif', '.png'}
    total_files = 0
    processed_files = 0
    report_data = []

    for root, _, files in os.walk(input_folder):
        for filename in files:
            total_files += 1
            input_path = os.path.join(root, filename)
            if any(filename.lower().endswith(ext) for ext in valid_extensions):
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                try:
                    new_filename = sanitize_filename(filename)
                    output_path = os.path.join(output_dir, new_filename)
                    with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
                        outfile.write(infile.read())
                    processed_files += 1
                    report_data.append([input_path, output_path, "Success"])
                    print(f"Renomeado: {input_path} -> {output_path}")
                except Exception as e:
                    report_data.append([input_path, "", f"Error: {e}"])
                    print(f"Erro ao processar {input_path}: {e}")
            else:
                report_data.append([input_path, "", "Skipped: Invalid file type"])

    # Generate CSV report
    report_path = os.path.join(output_folder, "conversion_report.csv")
    with open(report_path, mode='w', newline='', encoding='utf-8') as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["Original Path", "New Path", "Status"])
        writer.writerows(report_data)

    print(f"Total de arquivos: {total_files}")
    print(f"Arquivos processados: {processed_files}")
    print(f"Relatório gerado em: {report_path}")

if __name__ == "__main__":
    rename_images()
