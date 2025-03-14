import pytest
from pubmed_fetcher.fetcher import fetcher

def test_fetcher():
    result = fetcher("cancer")
    assert isinstance(result, list)
