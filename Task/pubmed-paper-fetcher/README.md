PubMed Industry Author Extractor

Overview

This project is a command-line tool that fetches research papers from PubMed based on a user-specified query and identifies papers with at least one author affiliated with a pharmaceutical or biotech company. The results are saved as a CSV file.

Features

Fetches papers using the PubMed API with support for full query syntax.

Identifies non-academic authors based on heuristic rules (e.g., email addresses, company names, or exclusion of academic institutions).

Outputs results in a CSV file with key details.

Provides command-line options for better usability.

Uses Poetry for dependency management and packaging.

Installation

Prerequisites

Ensure you have Python installed (>=3.7). Install dependencies using Poetry:

poetry install

Usage

Run the script using the command line:

poetry run get-papers-list "search query" --email your-email@example.com --file output.csv --debug

Command-line Options:

query: The search query for PubMed.

--email: Your email address (required by the NCBI Entrez API).

--file: The output CSV file (default: results.csv).

--debug: Enables debug mode to print additional details.

-h or --help: Displays usage instructions.

Output

The script generates a CSV file with the following columns:

PubmedID: Unique identifier for the paper.

Title: Title of the paper.

Publication Date: Date the paper was published.

Non-academic Author(s): Names of authors affiliated with non-academic institutions.

Company Affiliation(s): Names of pharmaceutical/biotech companies.

Corresponding Author Email: Email address of the corresponding author.

Code Organization

module/: Contains core functionality for fetching and filtering PubMed papers.

cli.py: Command-line interface for interacting with the module.

tests/: Unit tests for the module.

Tools & Libraries Used

BioPython - For accessing PubMed API.

Click - For handling command-line arguments.

Poetry - For dependency management and packaging.

Bonus Features

Modular structure: The program is split into a reusable module and a CLI tool.

Ready for publishing: The module can be published to TestPyPI.

License

This project is open-source and available under the MIT License.
