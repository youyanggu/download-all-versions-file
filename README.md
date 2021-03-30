# Download All Versions of a File from a GitHub Repository

This simple script enables users to quickly download all versions of a file (past & present) in a single branch of a GitHub repository, allowing them to run various analyses on all the file versions.

## Prerequisites

You must have Python 3 and the [`requests`](https://requests.readthedocs.io/en/master/) library installed. You can install the library by running the following command: `pip install requests`.

Unauthenticated clients can make a maximum of 60 requests per hour on the GitHub API. To get more requests per hour, we'll need to [authenticate](https://docs.github.com/en/rest/guides/getting-started-with-the-rest-api#authentication) using a personal access token. Once you have a token, please set it as your environment variable for `GITHUB_ACCESS_TOKEN` (for example, in your ~/.bashrc file).

## Usage Help

```
python download_all_versions.py --help
```

## Sample Usage

```
python download_all_versions.py --author CSSEGISandData --repo_name COVID-19 --branch master --file_path csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv --output_dir output_jhu_deaths --limit_by_day first
```

To avoid look-ahead bias in time series forecasting, we must only use the data that was available on the day the forecast is made. The above command download all historical versions of [JHU US Deaths Time Series data](https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv) from the Johns Hopkins CSSE repository: https://github.com/CSSEGISandData/COVID-19. It saves all versions to the `output_jhu_deaths` directory. If there are multiple versions on the same commit date, we take the first one.
