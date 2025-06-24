import requests
from bs4 import BeautifulSoup
import json

def scrape_academics(url):
    # Fetch HTML
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Locate the target table (example: first table)
    table = soup.find("table")
    if not table:
        raise ValueError("No <table> found on the page.")
    
    # Extract headings
    headers = []
    for th in table.find_all("th"):
        headers.append(th.get_text(strip=True))
    
    # Extract rows
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all(["td", "th"])
        if not cells:
            continue
        row = {}
        for header, cell in zip(headers, cells):
            row[header] = cell.get_text(strip=True)
        rows.append(row)
    
    return rows

if __name__ == "__main__":
    url = "https://biology.ed.ac.uk/people/academic/0"
    data = scrape_academics(url)
    print(json.dumps(data, indent=2))