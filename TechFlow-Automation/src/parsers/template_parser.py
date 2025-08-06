import csv

def parse_template(file_path):
    """
    Parses a CSV template file to extract structured data.

    Args:
        file_path (str): Path to the CSV template file.

    Returns:
        list[dict]: A list of dictionaries containing the extracted data.
    """
    extracted_data = []

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            extracted_data.append(row)

    return extracted_data

# Example usage
# template_data = parse_template('path_to_template.csv')
# print(template_data)
