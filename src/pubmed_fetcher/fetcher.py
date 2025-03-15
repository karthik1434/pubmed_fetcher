import requests
import csv
import re
import argparse
from typing import List, Dict, Optional
from xml.etree import ElementTree as ET

def fetcher(query: str, debug: bool = False) -> List[Dict]:
    """Fetch papers from PubMed API based on the given query."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 10}
    
    if debug:
        print(f"Fetching PubMed IDs for query: {query}")
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        pmids = data.get("esearchresult", {}).get("idlist", [])
        return fetch_paper_details(pmids, debug)
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

def fetch_paper_details(pmids: List[str], debug: bool = False) -> List[Dict]:
    """Fetch details and author affiliations for given PubMed IDs."""
    if not pmids:
        print("No PubMed IDs found for the given query.")
        return []
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "id": ",".join(pmids), "retmode": "xml"}
    
    if debug:
        print(f"Fetching details for PubMed IDs: {pmids}")
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.text)
    except requests.RequestException as e:
        print(f"Error fetching paper details: {e}")
        return []
    
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
            continue  # Skip papers without non-academic authors
        
        corresponding_author_email = extract_corresponding_author_email(article)
        
        papers.append({
            "PubmedID": pmid,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join([a["name"] for a in non_academic_authors]),
            "Company Affiliation(s)": ", ".join(set([a["affiliation"] for a in non_academic_authors])),
            "Corresponding Author Email": corresponding_author_email
        })
    
    return papers

def extract_email(affiliation: str) -> str:
    """Extract email from an affiliation string."""
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
    match = email_pattern.search(affiliation)
    return match.group(0) if match else ""

def extract_corresponding_author_email(article) -> str:
    """Extract corresponding author email from the PubMed XML."""
    email_pattern = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}")
    for affiliation in article.findall(".//AffiliationInfo/Affiliation"):
        match = email_pattern.search(affiliation.text if affiliation is not None else "")
        if match:
            return match.group(0)
    return ""

def identify_non_academic_authors(authors: List[Dict]) -> List[Dict]:
    """Identify non-academic authors based on affiliations."""
    company_keywords = ["Inc", "Ltd", "LLC", "Corporation", "Pharma", "Biotech", "Company", "Genentech", "Pfizer", "Novartis", "Roche", "AstraZeneca", "Merck"]
    academic_keywords = ["University", "Institute", "College", "Hospital", "Medical School"]
    email_company_patterns = re.compile(r"@([a-zA-Z0-9.-]+)\\.(com|net|org|co|biz)")
    
    return [author for author in authors if (any(kw in author["affiliation"] for kw in company_keywords) and not any(kw in author["affiliation"] for kw in academic_keywords)) or email_company_patterns.search(author["email"])]

def save_to_csv(papers: List[Dict], filename: Optional[str] = None):
    """Save fetched papers to a CSV file or print to console."""
    if not papers:
        print("No papers found with non-academic authors.")
        return
    
    if filename:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
    else:
        for paper in papers:
            print(paper)

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", type=str, help="Output CSV filename (optional)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    papers = fetcher(args.query, args.debug)
    save_to_csv(papers, args.file)

if __name__ == "__main__":
    main()