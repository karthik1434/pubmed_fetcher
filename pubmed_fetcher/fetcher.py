import requests
import csv
import re
from typing import List, Dict

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_papers(query: str) -> List[Dict]:
    """Fetch papers from PubMed based on the given query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 10,
        "retmode": "json"
    }
    response = requests.get(PUBMED_API_URL, params=params)
    response.raise_for_status()
    
    data = response.json()
    pubmed_ids = data.get("esearchresult", {}).get("idlist", [])

    return fetch_details(pubmed_ids)

def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch details of papers using PubMed IDs."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()

    data = response.json()
    results = []

    for pubmed_id in pubmed_ids:
        article = data.get("result", {}).get(pubmed_id, {})
        
        title = article.get("title", "N/A")
        pub_date = article.get("pubdate", "N/A")
        authors = article.get("authors", [])

        # Extract authors and filter non-academic ones
        non_academic_authors, company_affiliations = filter_non_academic_authors(authors)

        results.append({
            "PubMed ID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": "; ".join(non_academic_authors),
            "Company Affiliation(s)": "; ".join(company_affiliations),
            "Corresponding Author Email": extract_email(authors),
        })

    return results

def filter_non_academic_authors(authors: List[Dict]) -> (List[str], List[str]):
    """Identify non-academic authors and their company affiliations."""
    non_academic_authors = []
    company_affiliations = []

    academic_keywords = ["university", "college", "institute", "research center", "lab"]
    for author in authors:
        name = author.get("name", "Unknown")
        affiliation = author.get("affiliation", "").lower()

        if any(keyword in affiliation for keyword in academic_keywords):
            continue  # Skip academic authors
        if affiliation:
            non_academic_authors.append(name)
            company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations

def extract_email(authors: List[Dict]) -> str:
    """Extract email of the corresponding author."""
    for author in authors:
        if "email" in author:
            return author["email"]
    return "N/A"

def save_to_csv(results: List[Dict], filename: str):
    """Save results to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

if __name__ == "__main__":
    query = input("Enter search query: ")
    results = fetch_papers(query)
    
    if results:
        save_to_csv(results, "results.csv")
        print(f"Results saved to results.csv")
    else:
        print("No results found.")
