import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import pandas as pd

# Regex pattern for email addresses
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

# Replace with the URL of the webpage you want to scrape
# url = 'https://www.preprints.org/subject/browse/biology-and-life-sciences?id=16&name=Biology+and+Life+Sciences'
# url = 'https://www.biorxiv.org/collection/biochemistry'
# url = 'https://guides.lib.lsu.edu/c.php?g=962078&p=6948257'
# url = 'https://www.tmd.ac.jp/english/hpha/staff/'  - table data
# url = 'https://www.tus.ac.jp/en/labo/research_field/list.html?q=Biology'
# url = "https://crukcambridgecentre.org.uk/users/sujath-abbas"
url = "https://www.southampton.ac.uk/people/5x82lq/doctor-adriana-wilde"

def decompose_unwanted(soup):
    # Remove unwanted sections (header, footer, side menus)
    for tag in soup.find_all(['header', 'footer', 'nav', 'aside']):
        tag.decompose()
    pass

def extract_emails_from_href(url):
    emails = []
    response = requests.get(url)
    soup = BeautifulSoup(response, 'html.parser')
    email_links = soup.find_all('a', href=True)
    for link in email_links:
        href = link['href']
        print(href)
        if href.startswith('mailto:'):
            # Extract email using regex to clean it up just in case
            match = re.search(r'mailto:([^\?]+)', href)
            if match:
                emails.append(match.group(1))

def extract_emails_from_source(url):
    try:
        print("Website="+url)
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            source_code = response.text
            emails = re.findall(EMAIL_REGEX, source_code)
            if len(emails)>0:
                return list(set(emails))  # Remove duplicates
            else:
                return extract_emails_from_href(url)
        else:
            print(f"Failed to retrieve site: Status code {response.status_code}")
            return extract_emails_from_href(url)
    except Exception as e:
        print(f"Error: {e}")
        return []

def extract_author(url):
    # Send a GET request to fetch the raw HTML content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    decompose_unwanted(soup)
    # Look for meta tags with 'name' or 'property' attributes containing 'author'
    author_meta = soup.find_all('meta', attrs={'name': 'author'}) + \
                  soup.find_all('meta', attrs={'name': 'citation_author'}) + \
                  soup.find_all('meta', attrs={'name': 'og:title'}) + \
                  soup.find_all('meta', attrs={'property': 'og:title'}) + \
                  soup.find_all('meta', attrs={'property': 'foaf:name'}) + \
                  soup.find_all('meta', attrs={'itemprop': 'author'})

    # Extract and return the content of the author meta tags
    authors = [meta.get('content') for meta in author_meta if meta.get('content')]
    return authors if authors else []

# Extract title
def get_page_title(url):
    _headers_ = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        _headers_ = soup.find_all('meta', attrs={'name': 'title'}) +\
                    soup.find_all('meta', attrs={'name': 'citation_title'}) +\
                    soup.find_all('meta', attrs={'name': 'description'}) +\
                    soup.find_all('meta', attrs={'name': 'article_title'})
        header = [meta.get('content') for meta in _headers_ if meta.get('content')]
        return header
    except Exception as e:
        print(e)

# Extract description
def extract_description(url):
    _headers_ = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        _headers_ = soup.find_all('meta', attrs={'name': 'description'}) +\
                    soup.find_all('meta', attrs={'name': 'article_title'}) +\
                    soup.find_all('meta', attrs={'name': 'og:description'})
        header = [meta.get('content') for meta in _headers_ if meta.get('content')]
        return header
    except Exception as e:
        print(e)


# Extract phone number
def extract_phone_number(url):
    _headers_ = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        _headers_ = soup.find_all('meta', attrs={'name': 'og:phone_number'}) +\
                    soup.find_all('meta', attrs={'name': 'og:fax_number'}) +\
                    soup.find_all('meta', attrs={'name': 'phone'}) +\
                    soup.find_all('meta', attrs={'name': 'mobile'}) +\
                    soup.find_all('meta', attrs={'name': 'telephone'})
        header = [meta.get('content') for meta in _headers_ if meta.get('content')]
        return header
    except Exception as e:
        print(e)

# Extract department
def extract_department(url):
    _headers_ = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        _headers_ = soup.find_all('meta', attrs={'name': 'schoool'}) +\
                    soup.find_all('meta', attrs={'name': 'school_metatag'}) +\
                    soup.find_all('meta', attrs={'name': 'department'}) +\
                    soup.find_all('meta', attrs={'name': 'faculty_metatag'})
        header = [meta.get('content') for meta in _headers_ if meta.get('content')]
        return header
    except Exception as e:
        print(e)

# Extract country
def extract_country(url):
    _headers_ = ""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        _headers_ = soup.find_all('meta', attrs={'name': 'og:country_name'}) +\
                    soup.find_all('meta', attrs={'name': 'country_name'}) +\
                    soup.find_all('meta', attrs={'name': 'country'}) +\
                    soup.find_all('meta', attrs={'name': 'region'}) +\
                    soup.find_all('meta', attrs={'name': 'province'}) +\
                    soup.find_all('meta', attrs={'name': 'state'}) +\
                    soup.find_all('meta', attrs={'name': 'location'})
        header = [meta.get('content') for meta in _headers_ if meta.get('content')]
        return header
    except Exception as e:
        print(e)

def parse_download_link():
    try:
        print('Inside parse_link')
    except Exception as e:
        print(e)

def extract_emails_from_source(url):
    try:
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
 
def isValidURL(str):
    # Regex to check valid URL 
    regex = ("((http|https)://)(www.)?" +
             "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" +
             "{2,6}\\b([-a-zA-Z0-9@:%" +
             "._\\+~#?&//=]*)")
    p = re.compile(regex)
    if (str == None):
        return False
    if(re.search(p, str)):
        return True
    else:
        return False

def get_data(links_filtered):
    _response_data_ = []
    print('Inside get_data..')
    try:
        for link in links_filtered:
            print("Link="+link)
            if(isValidURL(link)):
                _heading_ = get_page_title(link)
                _emails_ = extract_emails_from_source(link)
                _author_ = extract_author(link)
                _description_ = extract_description(link)
                _phone_number_ = extract_phone_number(link)
                _department_ = extract_department(link)
                _country_ = extract_country(link)
                print('Title:       |'+str(_heading_))
                print('Emails:      |'+str(_emails_))
                print('Author:      |'+str(_author_))
                print('description: |'+str(_description_))
                print('phone_number:|'+str(_phone_number_))
                print('department:  |'+str(_department_))
                print('country:     |'+str(_country_))
                if len(_emails_)>0 and len(_author_)>0:
                    print('Website:|'+link)
                    # print('Title:  |'+max(_heading_, key=len))
                    data = {
                        "titles":_heading_,
                        "emails":_emails_,
                        "authors":_author_,
                        "link": link,
                        "description":_description_,
                        "phone":_phone_number_,
                        "department":_department_
                    }
                    if len(_emails_)>0 and len(_heading_)>0:
                        _response_data_.append(data)
                        print('Title:  |'+str(_heading_))
                        print('Emails: |'+str(_emails_))
                        print('Author: |'+str(_author_))
                    print('---------------------------')
        # unique_data = [dict(t) for t in {tuple(sorted(d.items())) for d in _response_data_}]
        print(_response_data_)
    except Exception as e:
        print(f"Error: {e}")
        return []
    return _response_data_

def web_scrapper(url):
    print('Inside web_scrapper..'+url)
    parsed_uri = urlparse(url)
    hostname = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    print("hostname="+hostname)
    # Send a GET request to fetch the page content
    response = requests.get(url)
    # print(response)
    soup = BeautifulSoup(response.text, 'html.parser')
    decompose_unwanted(soup)

    # Find all anchor tags with an href attribute
    links = soup.find_all('a', href=True)
    # print(links)
    links_filtered = []
    links_filtered.append(url)
    # Extract and print the href attribute of each link
    for link in links:
        if link['href'] == '/' or 'http://' in link['href'] or 'https://' in link['href'] or link['href'].endswith('/'): 
            continue
        else:
            link_final = str(hostname) + str(link['href'])
            if len(link['href'])>1 and str(link['href']).startswith('/'):
                link_final = str(hostname) + str(link['href'])
            else:
                link_final = str(url) + str(link['href'])
            # print(link_final)
            links_filtered.append(link_final)
    print(links_filtered)
    _response_data_ = get_data(links_filtered)
    return _response_data_

def parse_table_data(url):
    _response_data_ = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        decompose_unwanted(soup)
        staff_data = []
        tables = soup.find_all('table')
        for table in tables:
            headers = table.find_all('th')
            rows = table.find_all('tr')
            for row in rows:
                data = {}
                cols = row.find_all('td')
                if len(headers) == len(cols):
                    for i in range(len(headers)):
                        # print(str(headers[i].get_text(strip=True)) +" : "+str(cols[i].get_text(strip=True)))
                        data[str(headers[i].get_text(strip=True))] = str(cols[i].get_text(strip=True))
                    _response_data_.append(data)
        print(_response_data_)
    except Exception as e:
        print("Xception: parse_table_data="+e)
    return _response_data_

# url = "https://www.philosophie.lmu.de/en/directory-of-persons/"
# url = "https://www.tmd.ac.jp/english/hpha/staff/"
# parse_table_data(url)
# web_scrapper(url)