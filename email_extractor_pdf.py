import re
import requests
from bs4 import BeautifulSoup
import PyPDF2
import fitz
import os
import csv
from datetime import datetime

# Regex pattern for email
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
cur_date = datetime.today().strftime('%Y-%m-%d %H%M')

# Read all files in folder
def read_all_files(folder_path):
    data = []
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Check if it's a file (not a subfolder)
        if os.path.isfile(file_path):
            print(file_path)
            file_data = extract_emails_from_pdf(file_path)
            data.append(file_data)
    print(data)
    write_to_file(data)
    return 'Data file created at static/'+str(cur_date)+'.csv'

def write_to_file(data):
    # Choose CSV file name
    csv_file = 'static/'+str(cur_date)+'.csv'

    # Get the fieldnames from the keys of the first dictionary
    fieldnames = data[0].keys()

    # Write to CSV
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()     # Write the header row
        writer.writerows(data)   # Write all rows


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
            "department": extract_department_text(doc),
            "file": pdf_path
        }
        return data
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
    pdf_file_path = 'D:/Projects/Freelance/py-WebsiteScrapper/static/pdfs/2025-07-16/'

    # print("Emails from website:")
    # print(extract_emails_from_website(website_url))

    print("\nEmails from PDF:"+pdf_file_path)
    # print(extract_emails_from_pdf(pdf_file_path))
    # extract_paragraphs(pdf_file_path)
    # get_title(pdf_file_path)
    print(read_all_files(pdf_file_path))

