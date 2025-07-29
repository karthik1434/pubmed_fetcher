import pytest
from pubmed_fetcher.fetcher import fetcher, extract_email, identify_non_academic_authors

def test_extract_email():
    sample_affiliation = "Department of Oncology, Genentech Inc., South San Francisco, CA, USA. john.doe@genentech.com"
    assert extract_email(sample_affiliation) == "john.doe@genentech.com"

def test_identify_non_academic_authors():
    authors = [
        {"name": "John Doe", "affiliation": "Genentech Inc.", "email": "john.doe@genentech.com"},
        {"name": "Jane Smith", "affiliation": "Harvard University", "email": "jane@harvard.edu"}
    ]
    result = identify_non_academic_authors(authors)
    assert len(result) == 1
    assert result[0]["name"] == "John Doe"

@pytest.mark.parametrize("query", ["cancer", "machine learning", "covid-19"])
def test_fetcher_returns_results(query):
    papers = fetcher(query)
    assert isinstance(papers, list)
    if papers:  # Only check contents if not empty
        assert "PubmedID" in papers[0]
        assert "Title" in papers[0]
