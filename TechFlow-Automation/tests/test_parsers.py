import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.parsers.form_parser import parse_html_form

def test_parse_html_form():
    with open('data/forms/form_example.html', 'r', encoding='utf-8') as f:
        html = f.read()
    data = parse_html_form(html)
    print(data)

if __name__ == "__main__":
    test_parse_html_form()


