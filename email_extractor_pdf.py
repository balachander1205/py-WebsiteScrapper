import re
import requests
from bs4 import BeautifulSoup
import PyPDF2
import fitz

# Regex pattern for email
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

def extract_emails_from_text(text):
    return re.findall(EMAIL_REGEX, text)


# ---------Extract emails from PDF ---------
def extract_emails_from_pdf(pdf_path):
    _response_data_ = []
    emails = []
    descripsion = []
    doc = fitz.open(pdf_path)
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page_0 = reader.pages[0]
            document_info = reader.metadata
            # print(document_info)
            title = document_info.title
            # print(title)
            descripsion.append(page_0.extract_text())
            for page in reader.pages:
                text = page.extract_text()
                # print(text)
                if text:
                    emails.extend(extract_emails_from_text(text))
        data = {
            "emails": list(set(emails)),
            "description": extract_abstract_paragraph(doc),
            "title": get_title(doc),
            "department": extract_department_text(doc)
        }
        print(data)
        return _response_data_.append(data)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return []

# Extract pdf title
def get_title(doc):
    max_font_size = 0

    # First pass: find the maximum font size
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["text"].strip():
                            max_font_size = max(max_font_size, span["size"])

    # Second pass: collect all text with the max font size
    large_font_texts = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if span["size"] == max_font_size:
                            text = span["text"].strip()
                            if text:
                                large_font_texts.append(text)

    # Combine all large font texts into a single string
    combined_text = " ".join(large_font_texts)
    return combined_text

# Extarct department
def extract_department_text(doc):
    keyword = "department"
    matches = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    full_line = " ".join(span["text"] for span in line["spans"]).strip()
                    if keyword.lower() in full_line.lower():
                        matches.append({
                            "page": page_num,
                            "text": full_line
                        })

    if matches:
        for match in matches:
            return match['text']
    else:
        return ''

# Extract description from abstract string
def extract_abstract_paragraph(doc):
    abstract_started = False
    abstract_lines = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        
        for block in blocks:
            if "lines" not in block:
                continue

            for line in block["lines"]:
                line_text = " ".join(span["text"] for span in line["spans"]).strip()

                if not line_text:
                    continue

                if not abstract_started:
                    if line_text.lower().startswith("abstract"):
                        abstract_started = True
                        continue  # skip the heading itself
                else:
                    # Optional: stop if new heading is detected
                    if line_text.isupper() and len(line_text.split()) <= 5:
                        break
                    abstract_lines.append(line_text)

            if abstract_started and abstract_lines:
                continue  # collect remaining blocks on same page

        if abstract_started and abstract_lines:
            continue  # collect across pages if needed
    result_string = ""
    # Output lines
    if abstract_lines:
        for line in abstract_lines:
            if line.endswith('.'):
                result_string += str(line)
                break
            else:
                result_string += str(line)    
    return result_string


# --------- Example Usage ---------
if __name__ == "__main__":
    #website_url = 'https://www.preprints.org/subject/browse/biology-and-life-sciences?id=16&name=Biology+and+Life+Sciences'
    website_url = 'https://www.biorxiv.org/collection/biochemistry'
    # pdf_file_path = 'D:/Projects/Freelance/py-WebsiteScrapper-2/data/preprints202504.0818.v1.pdf'
    pdf_file_path = 'D:/Projects/Freelance/py-WebsiteScrapper/static/pdfs/2025-07-16/2025.07.10.664210v1.full.pdf'

    # print("Emails from website:")
    # print(extract_emails_from_website(website_url))

    print("\nEmails from PDF:"+pdf_file_path)
    print(extract_emails_from_pdf(pdf_file_path))
    # extract_paragraphs(pdf_file_path)
    # get_title(pdf_file_path)

