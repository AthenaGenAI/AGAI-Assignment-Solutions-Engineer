import sys
import os
sys.path.append('src/parsers')
from form_parser import parse_html_form
import json

# Test the form parser with Greek text
result = parse_html_form('data/forms/contact_form_2.html')
print(json.dumps(result, ensure_ascii=False, indent=2))
