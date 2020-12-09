import argparse
import datetime
import json
import os
import time
from multiprocessing import cpu_count
from threading import Thread

from collector import Collector, WebDriverException
from tweetDB import TweetDB

argv_parser = argparse.ArgumentParser()
# Search parameters
argv_parser.add_argument('-k', '--searchKey', type=str, required=True,
                         help="search key that will be searched")
argv_parser.add_argument('-s', '--start_date', type=str, required=True,
                         help="starting date for search in YYYY-MM-DD format")
argv_parser.add_argument('-e', '--end_date', type=str, required=True,
                         help="final date for search in YYYY-MM-DD format")
# Setting parameters
argv_parser.add_argument('-f', '--settings_file', type=bool, required=True, default=True,
                         help="use settings.json file (ignore setting parameters)")
argv_parser.add_argument('-u', '--username', type=str, required=False,
                         help="username of twitter account")
argv_parser.add_argument('-p', '--password', type=str, required=False,
                         help="password of twitter account")
argv_parser.add_argument('-d', '--chromedriver_path', type=str, required=False,
                         default='chromedriver',
                         help="chromedriver path that is used")
argv_parser.add_argument('-t', '--thread_count', type=int, default=0, required=False,
                         help="number of thread that is used in program")
argv_parser.add_argument('-m', '--missing_run_count', type=int, default=1, required=False,
                         help="re-run number for missings dates")
args = argv_parser.parse_args()

if args.settings_file:
    with open("settings.json", 'r') as settings_file:
        settings = json.load(settings_file)

    USERNAME = settings["username"]
    PASSWORD = settings["password"]

    CHROMEDRIVER_PATH = settings["chromedriver_path"]
    THREAD_COUNT = (settings["thread_count"]
                    if settings["thread_count"] else cpu_count() * 2 - 1)

    MISSING_DATES_TRIAL_COUNT = settings["missing_run_count"]
else:
    USERNAME = args.username
    PASSWORD = args.password

    CHROMEDRIVER_PATH = args.chromedriver_path
    THREAD_COUNT = args.thread_count if args.thread_count else cpu_count() * 2 - 1

    MISSING_DATES_TRIAL_COUNT = args.missing_run_count

if not os.path.isfile(CHROMEDRIVER_PATH):
    raise ValueError(f"missing chromedriver file: {CHROMEDRIVER_PATH}")

KEY = args.searchKey

DATE_START = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
DATE_END = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
DAY = datetime.timedelta(days=1)
STEP = 1

print(f"Collector is starting with {THREAD_COUNT} threads.")

db_conn = TweetDB(f"{KEY}_{DATE_START}-{DATE_END}")
db_conn.create_tables()

container_pool = [list() for _ in range(THREAD_COUNT)]


def get_missing_dates(reverse_sorted: bool = False) -> list:
    """Returns missing dates between DATE_START and DATE_END 
    that are fetched from database"""
    c = db_conn.conn.cursor()
    c.execute("SELECT DISTINCT post_date FROM Tweet")
    collected_dates = set([datetime.date.fromtimestamp(i[0])
                           for i in c.fetchall()])
    c.close()

    all_dates = set([DATE_START + datetime.timedelta(days=i)
                     for i in range((DATE_END-DATE_START).days)])

    return sorted(all_dates - collected_dates, reverse=reverse_sorted)


def search_tweets_by_date_to_container(date: datetime.date, container: list):
    """Main searching function that runs on thread"""
    collector = Collector(USERNAME, PASSWORD, chromePath=CHROMEDRIVER_PATH)

    from_ = date
    to_ = date + DAY*STEP

    print(f"Collecting {KEY}: {from_} - {to_}")

    try:
        collector.search(f"${KEY}", tabName='live', from_=from_, to_=to_)
        collector.retrieve_tweets_to_container(KEY, container)
    except WebDriverException as e:
        print(f"An error occured in browser:\n{str(e)}\nClosing browser...")
        collector.closeAll()
    finally:
        container_pool.append(container)


def container_collection(container: list):
    """pushes content of container to database and empties the container"""
    while len(container) > 0:
        db_conn.insert_tweet(container.pop())
    db_conn.conn.commit()


def collection_process(dates_list: list):
    """Searching process controller funtion. 
    Opens threads and manages containers"""
    while len(dates_list) > 0:
        if len(container_pool) > 0:
            process_container = container_pool.pop()
            container_collection(process_container)

            process_date = dates_list.pop()

            def target_func():
                search_tweets_by_date_to_container(process_date,
                                                   process_container)

            Thread(target=target_func).start()

        else:
            time.sleep(3)

    while len(container_pool) != THREAD_COUNT:
        time.sleep(3)

    for container in container_pool:
        container_collection(container)


t0 = time.time()

# extract dates
target_dates = sorted([DATE_START + datetime.timedelta(days=i)
                       for i in range((DATE_END-DATE_START).days)],
                      reverse=True)
# start collection
collection_process(target_dates)

# start collection for missing dates
for _ in range(MISSING_DATES_TRIAL_COUNT):
    missing_dates = get_missing_dates(reverse_sorted=True)
    print(f"Number of missing days: {len(missing_dates)}")

    if len(missing_dates) > 0:
        break

    collection_process(missing_dates)

print(f"Collector finished in {datetime.timedelta(seconds=time.time() - t0)}")
