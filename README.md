# Tweet Collector

Tweet Collection script that runs with selenium. Collect tweets of tags (#apple), stocks ($AAPL) and words (apple)

To collect large amount of tweet without struggling with Twitter, requires twitter account. (A verified one is strongly recommended.)

## Usage
    ```bash
        python tweet_collector.py --options
    ```
### Options:
 -  `h, --help`

 -  `-k, --searchKey KEY` (required)
    search key will be searched

 -  `-a, --search_as [tag, stock, word]` (default: _`tag`_)
    search method _`tag`_ -> _`$`_, _`stock`_ -> _`$`_ and _`word`_ is direct word search

 -  `-s, --start_date START_DATE` (required) 
    starting date for search in YYYY-MM-DD format

 -  `-e, --end_date END_DATE` (required)
    final date for search in YYYY-MM-DD format

 -  `-f, --settings_file BOOL` (required) (default: _`True`_)
    use settings.json file (ignore setting parameters)

 -  `-u, --username USERNAME`  
    username of twitter account

 -  `-p, --password PASSWORD`  
    password of twitter account

 -  `-d, --chromedriver_path CHROMEDRIVER_PATH` (default: _`chromedriver.exe`_)
    chromedriver path that is used 

 -  `-t, --thread_count THREAD_COUNT` (default: _`0`_)
    number of thread that is used in program 

 -  `-m, --missing_run_count MISSING_RUN_COUNT` (default: _`1`_)
    re-run number for missings dates 

### Examples
 - #### Using _settings.json_ file
    Example settings file
    ```json
    {
        "username": "*******",
        "password": "*******",
        "chromedriver_path": "chromedriver.exe",
        "thread_count": 0,
        "missing_run_count": 1
    }
    ```
    Running code
    ```bash
    python tweet_collector.py -k AAPL -a stock -s 2020-07-28 -e 2020-08-28 -f True
    ```
 - #### Without _settings.json_ file
    ```
    Running code
    ```bash
    python tweet_collector.py -k AAPL -a stock -s 2020-07-28 -e 2020-08-28 -f False -u ******* -p *******
    ```
## Requirements

- #### Python 3.6+ 
    _written in 3.7.9_

- #### Selenium 
    You can install by using *_[pip](https://pypi.org/project/selenium/)_*

- #### chromedriver
    You can get proper version from *_[chromedriver](https://chromedriver.chromium.org/downloads)_*

## License

[MIT](https://github.com/omer-metin/TweetCollector/blob/master/LICENSE.md)