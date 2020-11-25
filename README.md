# Tweet Collector

Tweet Collection script that runs with selenium. Collect tweets about stock companies (i.e. AAPL)

To collect large amount of tweet without struggling with Twitter, requires twitter account. (A verified one is strongly recommended.)

## Usage
    ```bash
        python tweet_collector.py --options
    ```
### Options:
 -  `h, --help`

 -  `-c COMPANY_TICKER, --company_ticker COMPANY_TICKER` (required)
    company ticker that will be searched

 -  `-s START_DATE, --start_date START_DATE` (required) 
    starting date for search in YYYY-MM-DD format

 -  `-e END_DATE, --end_date END_DATE` (required)
    final date for search in YYYY-MM-DD format

 -  `-u USERNAME, --username USERNAME` (required) 
    username of twitter account

 -  `-p PASSWORD, --password PASSWORD` (required) 
    password of twitter account

 -  `-d CHROMEDRIVER_PATH, --chromedriver_path CHROMEDRIVER_PATH` 
    chromedriver path that is used (default: `chromedriver`)

 -  `-t THREAD_COUNT, --thread_count THREAD_COUNT`  
    number of thread that is used in program (default: `0`)

 -  `-m MISSING_RUN_COUNT, --missing_run_count MISSING_RUN_COUNT`
    re-run number for missings dates (default: `1`)


# Requirements

- ### Selenium
    ```bash
    pip install selenium
    ```