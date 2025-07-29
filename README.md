# PubMed Fetcher

## Overview
PubMed Fetcher is a command-line tool that retrieves research papers from PubMed based on a user-specified query. It filters papers that have at least one author affiliated with a pharmaceutical or biotech company and outputs the results in CSV format.

## Features
- Fetches research papers from PubMed using the **Entrez API**.
- Identifies **non-academic authors** (from pharmaceutical or biotech companies) using heuristics.
- Outputs results as a **CSV file** with the following columns:
  - **PubmedID**: Unique identifier for the paper.
  - **Title**: Title of the paper.
  - **Publication Date**: Date of publication.
  - **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions.
  - **Company Affiliation(s)**: Names of pharmaceutical/biotech companies.
  - **Corresponding Author Email**: Email of the corresponding author.
- Supports **PubMed's full query syntax**.
- Provides **CLI options**:
  - `-h` or `--help`: Displays usage instructions.
  - `-d` or `--debug`: Enables debug mode for detailed logs.
  - `-f` or `--file`: Specifies the output filename (optional, prints to console if omitted).

## Installation
### Prerequisites
- **Python 3.11.9** or later
- **Poetry** (for dependency management)
- **Git** (for version control)

### Setup Instructions
1. **Clone the Repository**
   ```sh
   git clone https://github.com/karthik1434/pubmed_fetcher.git
   cd pubmed_fetcher
   ```
2. **Install Poetry (if not already installed)**
   ```sh
   pip install poetry
   ```
3. **Install Dependencies**
   ```sh
   poetry install
   ```

## Usage
### Activating the Virtual Environment
Before running the program, activate the Poetry virtual environment:
```sh
poetry env activate
```
If using **PowerShell**:
```powershell
poetry env activate powershell
```
If using **Command Prompt (cmd)**:
```cmd
poetry env activate cmd
```

Alternatively, you can run commands without activating the environment using `poetry run`.

### Fetching Research Papers
To fetch papers based on a query:
```sh
poetry run get-papers-list "cancer treatment" -f results.csv
```
This will **fetch papers**, **filter non-academic authors**, and **save results** to `results.csv`.

### Debug Mode
To enable debug mode:
```sh
poetry run get-papers-list "COVID-19 vaccine" -d
```

### Printing to Console
If `-f` is omitted, results will be printed to the console:
```sh
poetry run get-papers-list "diabetes research"
```

## Code Structure
```
pubmed_fetcher/
│── src/
│   ├── fetcher.py      # Handles API calls and data processing
│   ├── cli.py          # Command-line interface wrapper
│── tests/              # Contains unit tests
│── README.md          # Documentation
│── pyproject.toml      # Poetry configuration file
│── poetry.lock         # Dependency lock file
```

## Error Handling
- **API Failures**: Handles connection errors and invalid responses.
- **Empty Results**: Displays a message if no matching papers are found.
- **Invalid Input**: Ensures queries are properly formatted.

📁 tests/ – Test Suite for PubMed Fetcher
This directory contains unit tests for validating the functionality of the pubmed_fetcher Python package.

✅ What’s Covered
Email extraction

Ensures valid email addresses are correctly parsed from author affiliations.

Non-academic author identification

Verifies filtering logic based on company keywords and email domains.

End-to-end query tests

Confirms that fetching real papers from PubMed returns properly structured data.

🧪 Running Tests
You can run all tests using pytest. Make sure you're in the root of the project.

If you're using Poetry:
bash
Copy
Edit
poetry run pytest
Or using plain Python (outside Poetry):
bash
Copy
Edit
pip install -r requirements-dev.txt  # if applicable
pytest
📂 File Structure


