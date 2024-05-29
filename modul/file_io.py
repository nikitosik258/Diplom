def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_results_to_file(results, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(results)
