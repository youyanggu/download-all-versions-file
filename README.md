# Download All Versions of a File from a GitHub Repository

This simple script enables users to quickly download all versions of a file (past & present) in a single branch of a GitHub repository, allowing them to run various analyses on all the file versions.

## Prerequisites

You must have Python 3 and the [`requests`](https://requests.readthedocs.io/en/master/) library installed. You can install the library by running the following command: `pip install requests`.

Unauthenticated clients can make a maximum of 60 requests per hour on the GitHub API. To get more requests per hour, we'll need to [authenticate](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authentication) using a personal access token.

## Usage Help

```
python download_all_versions.py --help
```

## Sample Usage

```
python download_all_versions.py --author youyanggu --repo_name covid19_projections --branch gh-pages --file_path index.md --output_dir output --limit_by_day last
```

The above command download all versions of [index.md](https://github.com/youyanggu/covid19_projections/blob/gh-pages/index.md) from the `gh-pages` branch of the following repo: https://github.com/youyanggu/covid19_projections. Saves all versions to the `output` directory. If there are multiple versions on the same commit date, we take the last one.
