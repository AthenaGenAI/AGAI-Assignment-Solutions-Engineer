import os
import sys

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from parsers.form_parser import parse_html_form

def test_parser():
    forms_dir = "../../dummy_data/forms/"  # Correct relative path to the forms directory
    for form_file in os.listdir(forms_dir):
        if form_file.endswith(".html"):
            form_path = os.path.join(forms_dir, form_file)
            form_data = parse_html_form(form_path)
            print(f"Data extracted from {form_file}: {form_data}")

if __name__ == "__main__":
    test_parser()