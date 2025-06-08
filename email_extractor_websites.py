import re
import requests

# Regex pattern for email addresses
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def extract_emails_from_source(url):
    try:
        print("Website="+url)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            source_code = response.text
            emails = re.findall(EMAIL_REGEX, source_code)
            return list(set(emails))  # Remove duplicates
        else:
            print(f"Failed to retrieve site: Status code {response.status_code}")
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []


if __name__ == "__main__":
    url = 'https://www.preprints.org/subject/browse/biology-and-life-sciences?id=16&name=Biology+and+Life+Sciences'
    # url = 'https://www.biorxiv.org/collection/biochemistry'
    found_emails = extract_emails_from_source(url)
    print(f"Emails found in {url}:\n", found_emails)