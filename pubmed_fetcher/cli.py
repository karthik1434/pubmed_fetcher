import argparse
import csv
from pubmed_fetcher.fetcher import fetch_pubmed_results, fetch_pubmed_paper_details

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name", default=None)
    args = parser.parse_args()

    print(f"Fetching results for query: {args.query}")
    paper_ids = fetch_pubmed_results(args.query)
    
    results = [fetch_pubmed_paper_details(pubmed_id) for pubmed_id in paper_ids]

    if args.file:
        with open(args.file, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"Results saved to {args.file}")
    else:
        for result in results:
            print(result)

if __name__ == "__main__":
    main()
