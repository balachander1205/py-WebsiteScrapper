import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
from datetime import datetime

headers = {"User-Agent": "Mozilla/5.0"}

cur_date = datetime.today().strftime('%Y-%m-%d')

def download_pdfs_from_page(page_url, download_dir='static/pdfs/'+cur_date):
    os.makedirs(download_dir, exist_ok=True)
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    pdf_links = [urljoin(page_url, link['href']) for link in soup.find_all('a', href=True) if link['href'].lower().endswith('.pdf')]

    for pdf_url in pdf_links:
        filename = os.path.join(download_dir, pdf_url.split('/')[-1])
        try:
            pdf_response = requests.get(pdf_url)
            print(pdf_response)
            if pdf_response.status_code == 200:
                with open(filename, 'wb') as f:
                    f.write(pdf_response.content)
                print(f'Downloaded: {filename}')
            else:
                print(f'Failed to download: {pdf_url}')
        except Exception as e:
            print(f'Error downloading {pdf_url}: {e}')

# Example usage
page_url = 'https://www.biorxiv.org/content/10.1101/2025.07.10.664210v1'
download_pdfs_from_page(page_url)