import re
import requests
from bs4 import BeautifulSoup
import PyPDF2

# Regex pattern for email
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def extract_emails_from_text(text):
    return re.findall(EMAIL_REGEX, text)


# ---------Extract emails from PDF ---------
def extract_emails_from_pdf(pdf_path):
    emails = []
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            document_info = reader.metadata
            print(document_info)
            title = document_info.title
            print(title)
            for page in reader.pages:
                text = page.extract_text()
                # print(text)
                if text:
                    emails.extend(extract_emails_from_text(text))
        return list(set(emails))
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

# --------- Example Usage ---------
if __name__ == "__main__":
    #website_url = 'https://www.preprints.org/subject/browse/biology-and-life-sciences?id=16&name=Biology+and+Life+Sciences'
    website_url = 'https://www.biorxiv.org/collection/biochemistry'
    pdf_file_path = 'D:/Projects/Freelance/py-WebsiteScrapper-2/data/preprints202504.0818.v1.pdf'

    # print("Emails from website:")
    # print(extract_emails_from_website(website_url))

    print("\nEmails from PDF:"+pdf_file_path)
    print(extract_emails_from_pdf(pdf_file_path))
