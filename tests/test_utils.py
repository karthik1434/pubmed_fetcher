import pytest
from pubmed_fetcher.utils import extract_email, identify_non_academic_authors

def test_extract_email():
    assert extract_email("Dr. John Doe, johndoe@biotech.com") == "johndoe@biotech.com"
    assert extract_email("No email here") == ""

def test_identify_non_academic_authors():
    authors = [
        {"name": "Alice", "affiliation": "Biotech Inc", "email": "alice@biotech.com"},
        {"name": "Bob", "affiliation": "Harvard University", "email": "bob@harvard.edu"}
    ]
    result = identify_non_academic_authors(authors)
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
