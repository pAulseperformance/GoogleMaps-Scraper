import re
def extract_business_data(html_content):
    data = {}

    # Extract phone numbers
    # data['phone_numbers'] = re.findall(r'\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}', html_content)

    # Extract email addresses
    # data['emails'] = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_content)

    # # Extract ratings
    # data['ratings'] = re.findall(r'\b\d\.\d(?=\s*stars?)', html_content)

    # # Extract review counts
    # data['reviews'] = re.findall(r'\b\d+(?=\s*reviews?)', html_content)

    # # Extract addresses
    # data['addresses'] = re.findall(r'\d{1,5}\s\w+(\s\w+)*,\s\w+(\s\w+)*,\s[A-Z]{2}\s\d{5}', html_content)

    # # Extract website URLs
    # data['websites'] = re.findall(r'https?:\/\/(www\.)?[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', html_content)
    data['websites'] = re.findall(r'https?:\/\/[^\/]+', html_content)

    # # Extract business names
    # data['business_names'] = re.findall(r'"([^"]+)"|([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', html_content)

    # # Extract opening hours
    # data['opening_hours'] = re.findall(r'\b\d{1,2}:\d{2}\s?(AM|PM)\s?-\s?\d{1,2}:\d{2}\s?(AM|PM)', html_content)

    # # Extract prices
    # data['prices'] = re.findall(r'\${1,5}', html_content)

    # # Extract latitude and longitude
    # data['coordinates'] = re.findall(r'-?\d{1,3}\.\d+,\s?-?\d{1,3}\.\d+', html_content)

    return data




def load_mock_html(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()
for i in range(0, 9):
    # Load the mock HTML file
    mock_html = load_mock_html(f"mock_data/business_{i}.html")
    # Extract business data from the HTML
    business_data = extract_business_data(mock_html)
    print(business_data)
# mock_html = load_mock_html("mock_data/business_2.html")
# business_data = extract_business_data(mock_html)
print(business_data)