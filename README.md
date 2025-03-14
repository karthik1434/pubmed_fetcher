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
- **pip** (Python package manager)
- **Git** (for version control)

### Setup Instructions
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/pubmed_fetcher.git
   cd pubmed_fetcher
   ```
2. **Create a Virtual Environment** (optional but recommended)
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

## Usage
### Fetching Research Papers
To fetch papers based on a query:
```sh
python src/cli.py "cancer treatment" -f results.csv
```
This will **fetch papers**, **filter non-academic authors**, and **save results** to `results.csv`.

### Debug Mode
To enable debug mode:
```sh
python src/cli.py "COVID-19 vaccine" -d
```

### Printing to Console
If `-f` is omitted, results will be printed to the console:
```sh
python src/cli.py "diabetes research"
```

## Code Structure
```
pubmed_fetcher/
│── src/
│   ├── fetcher.py      # Handles API calls and data processing
│   ├── cli.py          # Command-line interface wrapper
│── tests/              # Contains unit tests
│── README.md          # Documentation
│── requirements.txt    # Dependencies
```

## Error Handling
- **API Failures**: Handles connection errors and invalid responses.
- **Empty Results**: Displays a message if no matching papers are found.
- **Invalid Input**: Ensures queries are properly formatted.

## Contributing
If you would like to contribute, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License.

---
For any questions, contact [your email or GitHub profile].

