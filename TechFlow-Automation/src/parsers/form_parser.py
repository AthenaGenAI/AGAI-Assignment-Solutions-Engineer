from bs4 import BeautifulSoup

def parse_html_form(file_path):
    """
    Parses an HTML form file to extract contact information.

    Args:
        file_path (str): Path to the HTML form file.

    Returns:
        dict: Extracted contact information.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    results = {
        "name": "",
        "email": "",
        "phone": "",
        "company": "",
        "service": "",
        "message": "",
        "submitted_at": "",
        "priority": ""
    }

    # Extract fields based on form structure
    name_field = soup.find('input', {'name': 'full_name'})
    email_field = soup.find('input', {'name': 'email'})
    phone_field = soup.find('input', {'name': 'phone'})
    company_field = soup.find('input', {'name': 'company'})
    service_field = soup.find('select', {'name': 'service'})
    message_field = soup.find('textarea', {'name': 'message'})
    submitted_at_field = soup.find('input', {'name': 'submission_date'})
    priority_field = soup.find('select', {'name': 'priority'})

    if name_field and name_field.get('value'):
        results['name'] = name_field['value']
    if email_field and email_field.get('value'):
        results['email'] = email_field['value']
    if phone_field and phone_field.get('value'):
        results['phone'] = phone_field['value']
    if company_field and company_field.get('value'):
        results['company'] = company_field['value']
    if service_field:
        selected_service = service_field.find('option', {'selected': True})
        if not selected_service:
            selected_service = service_field.find('option', selected=True)
        if selected_service:
            results['service'] = selected_service.text.strip()
    if message_field and message_field.text:
        results['message'] = message_field.text.strip()
    if submitted_at_field and submitted_at_field.get('value'):
        results['submitted_at'] = submitted_at_field['value']
    if priority_field:
        selected_priority = priority_field.find('option', {'selected': True})
        if not selected_priority:
            selected_priority = priority_field.find('option', selected=True)
        if selected_priority:
            results['priority'] = selected_priority.text.strip()

    return results

# Example usage
# form_data = parse_html_form('path_to_form.html')
# print(form_data)