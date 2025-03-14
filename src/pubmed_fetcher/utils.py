import os
import requests
import csv
import re
from typing import List, Dict, Optional

def fetcher(query: str) -> List[Dict]:
    """Fetch papers from PubMed API based on the given query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Limit to 10 results for now
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    pmids = data.get("esearchresult", {}).get("idlist", [])
    return fetch_paper_details(pmids)

def fetch_paper_details(pmids: List[str]) -> List[Dict]:
    """Fetch details and author affiliations for given PubMed IDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    from xml.etree import ElementTree as ET
    root = ET.fromstring(response.text)
    
    papers = []
    for article in root.findall(".//PubmedArticle"):
        pmid = article.find(".//PMID").text
        title = article.find(".//ArticleTitle").text
        pub_date = article.find(".//PubDate/Year")
        pub_date = pub_date.text if pub_date is not None else "N/A"
        
        authors = []
        for author in article.findall(".//Author"):
            last_name = author.find("LastName")
            fore_name = author.find("ForeName")
            affiliation = author.find("AffiliationInfo/Affiliation")
            
            authors.append({
                "name": f"{fore_name.text} {last_name.text}" if fore_name is not None and last_name is not None else "Unknown",
                "affiliation": affiliation.text if affiliation is not None else "",
                "email": extract_email(affiliation.text if affiliation is not None else "")
            })
        
        non_academic_authors = identify_non_academic_authors(authors)
        company_authors = ", ".join([a["name"] for a in non_academic_authors])
        company_affiliations = ", ".join(set([a["affiliation"] for a in non_academic_authors]))
        corresponding_email = next((a["email"] for a in non_academic_authors if a["email"]), "")

        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": company_authors,
            "Company Affiliation(s)": company_affiliations,
            "Corresponding Author Email": corresponding_email
        })
    
    return papers

def extract_email(affiliation: str) -> str:
    """Extract email from an affiliation string."""
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
    match = email_pattern.search(affiliation)
    return match.group(0) if match else ""

def identify_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    """Identify non-academic authors based on affiliations."""
    non_academic = []
    company_keywords = ["Inc", "Ltd", "LLC", "Corporation", "Pharma", "Biotech", "Company"]
    email_company_patterns = re.compile(r"@([a-zA-Z0-9.-]+)\.(com|net|org|co|biz)")

    for author in authors:
        if any(keyword in author["affiliation"] for keyword in company_keywords) or email_company_patterns.search(author["email"]):
            non_academic.append(author)
    
    return non_academic

def save_to_csv(papers: List[Dict], results.csv: str):
    """Save fetched papers to a CSV file."""
    with open(results.csv, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

def validate_csv(results.csv: str) -> bool:
    """Validate if the CSV file matches the expected format."""
    expected_fields = ["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"]
    
    if not os.path.exists(results.csv):
        print(f"Error: {results.csv} not found.")
        return False

    with open(results.csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != expected_fields:
            print("Error: CSV format does not match expected fields.")
            return False
        
        for row in reader:
            if not all(row[field] for field in expected_fields):
                print(f"Error: Missing data in row {row}")
                return False

    print("CSV validation passed.")
    return True

def main():
    query = input("Enter search query: ")
    papers = fetcher(query)
    filename = "results.csv"
    save_to_csv(papers, filename)
    print(f"Results saved to {filename}")

    if validate_csv(filename):
        print("CSV file is valid.")
    else:
        print("CSV file validation failed.")

if __name__ == "__main__":
    main()
