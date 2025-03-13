import requests
import csv
import logging
from typing import List, Dict

PUBMED_API_URL = "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/"

def fetch_papers(query: str) -> List[Dict]:
    logging.debug(f"Fetching papers with query: {query}")
    response = requests.get(PUBMED_API_URL, params={"format": "json", "query": query})
    response.raise_for_status()
    
    papers = response.json().get("records", [])
    filtered_papers = filter_papers(papers)
    
    return filtered_papers

def filter_papers(papers: List[Dict]) -> List[Dict]:
    filtered_papers = []
    for paper in papers:
        authors = paper.get("authors", [])
        non_academic_authors = [author for author in authors if is_non_academic_author(author)]
        if non_academic_authors:
            filtered_papers.append({
                "PubmedID": paper.get("uid"),
                "Title": paper.get("title"),
                "Publication Date": paper.get("pubdate"),
                "Non-academic Author(s)": [author.get("name") for author in non_academic_authors],
                "Company Affiliation(s)": [author.get("affiliation") for author in non_academic_authors],
                "Corresponding Author Email": get_corresponding_author_email(paper)
            })
    return filtered_papers

def is_non_academic_author(author: Dict) -> bool:
    affiliation = author.get("affiliation", "").lower()
    return "pharma" in affiliation or "biotech" in affiliation

def get_corresponding_author_email(paper: Dict) -> str:
    for author in paper.get("authors", []):
        if author.get("corresponding"):
            return author.get("email", "")
    return ""

def save_to_csv(papers: List[Dict], filename: str):
    logging.debug(f"Saving papers to CSV file: {filename}")
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "PubmedID", "Title", "Publication Date", "Non-academic Author(s)", 
            "Company Affiliation(s)", "Corresponding Author Email"])
        writer.writeheader()
        for paper in papers:
            writer.writerow(paper)