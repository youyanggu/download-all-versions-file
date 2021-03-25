# Download All File Versions

This repo contains a script that enables you to download all versions of a file (past and present) in a GitHub repository.

## Prerequisites

You must have Python 3 and the `[requests](https://requests.readthedocs.io/en/master/)` library installed. You can install the library by running the following command: `pip install requests`.

## Usage Help

`python download_all_versions.py --help`

## Sample Usage

`python download_all_versions.py --author youyanggu --repo_name covid19_projections --branch gh-pages --file_path index.md --output_dir output --limit_by_day last`
