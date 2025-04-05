import click
from Bio import Entrez
import xml.etree.ElementTree as ET
import csv
import re

# List of keywords related to pharma/biotech companies
INDUSTRY_KEYWORDS = [
    "pharma", "pharmaceutical", "biotech", "biotechnology", "therapeutics",
    "inc", "ltd", "llc", "corporation", "company", "gmbh", "co.", "s.a.", "s.p.a."
]

# Function to check if an affiliation mentions an industry organization
def is_industry_affiliation(affiliation):
    affiliation_lower = affiliation.lower()
    return any(keyword in affiliation_lower for keyword in INDUSTRY_KEYWORDS)

# Extract author affiliations and check for industry

def extract_industry_authors(article):
    industry_authors = []
    article_title = article.findtext(".//ArticleTitle")

    for author in article.findall(".//Author"):
        lastname = author.findtext("LastName")
        forename = author.findtext("ForeName")
        affiliation = author.findtext(".//Affiliation")

        if lastname and forename and affiliation:
            full_name = f"{forename} {lastname}"
            if is_industry_affiliation(affiliation):
                industry_authors.append((full_name, affiliation, article_title))
    return industry_authors

# Fetch details of articles from PubMed

def fetch_pubmed_details(pubmed_ids, debug=False):
    Entrez.email = "your-email@example.com"  # Replace with your email

    handle = Entrez.efetch(db="pubmed", id=pubmed_ids, rettype="xml")
    data = handle.read()
    handle.close()

    # Decode bytes to string
    data_str = data.decode("utf-8")

    # Save raw response for debugging
    with open("raw_response.xml", "w", encoding="utf-8") as f:
        f.write(data_str)

    # Try parsing XML safely
    try:
        root = ET.fromstring(data_str)
    except ET.ParseError as e:
        print(f"Error parsing response: {e}")
        return []

    articles = []
    for article in root.findall(".//PubmedArticle"):
        if debug:
            print(ET.tostring(article, encoding="unicode"))
        articles.append(article)

    return articles

@click.command()
@click.argument("query")
@click.option("--email", default="your-email@example.com", help="Email for NCBI Entrez API")
@click.option("--file", default="results.csv", help="CSV file to save results")
@click.option("--debug", is_flag=True, help="Print debug info")
def fetch_papers(query, email, file, debug):
    print(f"Searching PubMed for query: {query}")
    Entrez.email = email
    handle = Entrez.esearch(db="pubmed", term=query, retmax=50)
    record = Entrez.read(handle)
    handle.close()

    pubmed_ids = record["IdList"]
    if debug:
        print(f"PubMed IDs: {pubmed_ids}")

    print("Fetching paper details from PubMed...")
    articles = fetch_pubmed_details(pubmed_ids, debug)

    results = []
    for article in articles:
        results.extend(extract_industry_authors(article))

    if not results:
        print("No industry-affiliated authors found in the retrieved papers.")
        return

    print(f"Found {len(results)} authors with industry affiliation. Saving to {file}...")
    with open(file, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Author", "Affiliation", "Article Title"])
        writer.writerows(results)

    print("Done!")

if __name__ == "__main__":
    fetch_papers()