import pytest
from pubmed_fetcher.fetcher import fetch_papers

def test_fetch_papers():
    result = fetch_papers("cancer")
    assert isinstance(result, list)
