"""
Downloads all versions of a file in a GitHub repository.

"""

import argparse
import datetime
import json
import os

import requests


def str_to_date(date_str, fmt='%Y-%m-%d'):
    """Convert string date to date object."""
    return datetime.datetime.strptime(date_str, fmt).date()


def str_to_datetime(date_str, fmt='%Y-%m-%dT%H:%M:%SZ'):
    """Convert string date to datetime object."""
    return datetime.datetime.strptime(date_str, fmt)


def get_headers():
    """
    GitHub API only allows 60 calls per hour from an unauthorized IP.

    To authenticate, you need to create a personal access token:
    https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token

    After creating the token, set it as an environment variable GITHUB_ACCESS_KEY

    More details about authentication:
    https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authentication
    """
    try:
        access_token = os.environ['GITHUB_ACCESS_TOKEN']
        return {
            'Authorization' : f"token {access_token}",
        }
    except KeyError:
        return None


def run_download(author, repo_name, branch, file_path, output_dir,
        limit_by_day=None, overwrite=False):
    """
    Sample usage:
    `python download_all_versions.py --author youyanggu --repo_name covid19_projections --branch gh-pages --file_path index.md --output_dir output --limit_by_day last`

    """
    print('====================================')
    print(datetime.datetime.now())
    print('Downloading all versions...')
    url = f'https://api.github.com/repos/{author}/{repo_name}/commits'
    print('URL:', url)
    print('Branch:', branch)
    print('File:', file_path)
    print('Output dir:', output_dir)
    print('Limit by day:', limit_by_day)
    print('Overwrite:', overwrite)

    assert limit_by_day in [None, 'first', 'last'], limit_by_day

    os.makedirs(output_dir, exist_ok=True)

    if get_headers():
        print('Using personal GitHub access token (max 5000 calls per hour)')
    else:
        print(('Missing GitHub access token. '
            'Using unauthenticated GitHub requests (max 60 calls per hour)'))

    # retrieve information about all commits that modified the file we want
    all_commits = []
    page = 0
    while True:
        page += 1
        print(f'{file_path} - Fetching page {page}...')
        r = requests.get(url,
            headers = get_headers(),
            params = {
                'sha' : branch,
                'path': file_path,
                'page': str(page),
                'per_page' : 1000, # max is 100, default is 30
            }
        )

        if not r.ok or r.text == '[]':
            if not r.ok:
                print(r, r.text)
            break

        all_commits += json.loads(r.text or r.content)
        print('Num commits:', len(all_commits))

    print('Final num commits:', len(all_commits))

    if limit_by_day:
        # date of each commit, in reverse chronological order
        commit_dates = [
            str_to_date(commit['commit']['author']['date'][0:10]) for commit in all_commits
        ]

        if limit_by_day == 'first':
            # We must reverse the order so it is chronologically increasing
            commit_dates = commit_dates[::-1]
    else:
        commit_dates = [
            str_to_datetime(commit['commit']['author']['date']) for commit in all_commits
        ]

    commit_date_to_sha_and_fname = {}
    for i, commit_date in enumerate(commit_dates):
        commit_date_str = str(commit_date).replace(' ', '_').replace(':', '')
        result_path =  f'{output_dir}/{file_path}_{commit_date_str}'
        if commit_date not in commit_date_to_sha_and_fname:
            commit_date_to_sha_and_fname[commit_date] = (all_commits[i]['sha'], result_path)

    assert list(sorted(commit_date_to_sha_and_fname.keys(), reverse=True)) == \
        list(commit_date_to_sha_and_fname.keys()), 'dict is not sorted'


    for commit_date, sha_and_fname in reversed(commit_date_to_sha_and_fname.items()):
        commit_sha, result_path = sha_and_fname

        if os.path.isfile(result_path):
            if overwrite:
                print('File exists, overwriting:', reslut_path)
            else:
                print('File exists, skipping:', result_path)
                continue

        url = requests.utils.requote_uri(
            f'https://raw.githubusercontent.com/{author}/{repo_name}/{commit_sha}/{file_path}')

        resp = requests.get(url, headers=get_headers())

        assert len(resp.text) > 0, resp

        with open(result_path, 'w') as f:
            f.write(resp.text)

        print('Saved to:', result_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--author', help='Author name', required=True)
    parser.add_argument('--repo_name', help='Repo name', required=True)
    parser.add_argument('--branch', help='Branch name', default='main')
    parser.add_argument('--file_path', help='Path of file in repo', required=True)
    parser.add_argument('--output_dir', help='Output directory location', required=True)
    parser.add_argument('--limit_by_day', help=('If you only want to keep the first or'
        ' last file on each commit date, specify `first` or `last`'), choices=['first', 'last'])
    parser.add_argument('-o', '--overwrite', action='store_true', help='Overwrite files')
    args = parser.parse_args()

    run_download(
        args.author,
        args.repo_name,
        args.branch,
        args.file_path,
        args.output_dir,
        args.limit_by_day,
        args.overwrite,
    )

    print('--------------------')
    print('Done', datetime.datetime.now())
