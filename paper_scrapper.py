from paperscraper.get_dumps import preprints_org

# Download metadata dump for Preprints.org
preprints_org()

import json

# Load the metadata dump
with open('preprints_org.jsonl', 'r') as file:
    for line in file:
        paper = json.loads(line)
        title = paper.get('title', 'No title available')
        authors = paper.get('authors', [])
        affiliations = paper.get('affiliations', [])
        emails = paper.get('emails', [])

        # Print or process the extracted information
        print(f"Title: {title}")
        for author, affiliation, email in zip(authors, affiliations, emails):
            print(f"Author: {author}, Affiliation: {affiliation}, Email: {email}")