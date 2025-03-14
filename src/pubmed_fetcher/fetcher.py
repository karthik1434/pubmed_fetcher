import requests
import csv
import re
import os
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET

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
    
    root = ET.fromstring(response.text)
    papers = []

    for article in root.findall(".//PubmedArticle"):
        pmid_elem = article.find(".//PMID")
        title_elem = article.find(".//ArticleTitle")
        pub_date_elem = article.find(".//PubDate/Year")

        pmid = pmid_elem.text if pmid_elem is not None else "N/A"
        title = title_elem.text if title_elem is not None else "N/A"
        pub_date = pub_date_elem.text if pub_date_elem is not None else "N/A"

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
        
        if not non_academic_authors:
            continue  # SKIP papers with NO non-academic authors

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
    company_keywords = ["Inc", "Ltd", "LLC", "Corporation", "Pharma", "Biotech", "Company", 
                        "Genentech", "Pfizer", "Novartis", "Roche", "AstraZeneca", "Merck"]
    email_company_patterns = re.compile(r"@([a-zA-Z0-9.-]+)\.(com|net|org|co|biz)")

    for author in authors:
        if any(keyword in author["affiliation"] for keyword in company_keywords) or email_company_patterns.search(author["email"]):
            non_academic.append(author)
    
    return non_academic

def save_to_csv(papers: List[Dict], filename: str):
    """Save fetched papers to a CSV file."""
    if not papers:
        print("No papers found with non-academic authors.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

def main():
    query = input("Enter search query: ")
    papers = fetcher(query)
    save_to_csv(papers, "pubmed_results.csv")
    print("Results saved to pubmed_results.csv")

if __name__ == "__main__":
    main()
