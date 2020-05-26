import argparse
import datetime
import time
from multiprocessing import cpu_count
from threading import Thread

from collector import Collector, WebDriverException
from tweetDB import TweetDB

argv_parser = argparse.ArgumentParser()
argv_parser.add_argument('-c', '--company_ticker', type=str, required=True,
                         help="company ticker that will be searched")
argv_parser.add_argument('-s', '--start_date', type=str, required=True,
                         help="starting date for search as YYYY-MM-DD")
argv_parser.add_argument('-e', '--end_date', type=str, required=True,
                         help="final date for search as YYYY-MM-DD")
argv_parser.add_argument('-u', '--username', type=str, required=True,
                         help="username of twitter account")
argv_parser.add_argument('-p', '--password', type=str, required=True,
                         help="password of twitter account")
argv_parser.add_argument('-d', '--chromedriver_path', type=str,
                         default='chromedriver',
                         help="chromedriver path that is used")
argv_parser.add_argument('-t', '--thread_count', type=int, default=0,
                         help="number of thread that is used in program")
argv_parser.add_argument('-m', '--missing_run_count', type=int, default=1,
                         help="re-run number for missings dates")
args = argv_parser.parse_args()


USERNAME = args.username
PASSWORD = args.password

CHROMEDRIVER_PATH = args.chromedriver_path
THREAD_COUNT = args.thread_count if args.thread_count else (cpu_count()-1) * 2

TICKER = args.company_ticker

DATE_START = datetime.datetime.strptime(args.start_date, "%Y-%m-%d").date()
DATE_END = datetime.datetime.strptime(args.end_date, "%Y-%m-%d").date()
DAY = datetime.timedelta(days=1)
STEP = 1

MISSING_DATES_TRIAL_COUNT = args.missing_run_count

print(f"Collector is starting with {THREAD_COUNT} threads.")

db_conn = TweetDB(f"TICKER_{DATE_START}-{DATE_END}")
db_conn.create_tables()

container_pool = [list() for _ in range(THREAD_COUNT)]


def get_missing_dates(reverse_sorted: bool = False) -> list:
    c = db_conn.conn.cursor()
    c.execute("SELECT DISTINCT post_date FROM Tweet")
    collected_dates = set([datetime.date.fromtimestamp(i[0])
                           for i in c.fetchall()])
    c.close()

    all_dates = set([DATE_START + datetime.timedelta(days=i)
                     for i in range((DATE_END-DATE_START).days)])

    return sorted(all_dates - collected_dates, reverse=reverse_sorted)


def search_tweets_by_date_to_container(date: datetime.date, container: list):
    collector = Collector(USERNAME, PASSWORD, chromePath=CHROMEDRIVER_PATH)

    from_ = date
    to_ = date + DAY*STEP

    print(f"Collecting {TICKER}: {from_} - {to_}")

    try:
        collector.search(f"${TICKER}", tabName='live', from_=from_, to_=to_)
        collector.retrieve_tweets_to_container(TICKER, container)
    except WebDriverException as e:
        print(f"An error occured in browser:\n{str(e)}\nClosing browser...")
        collector.closeAll()
    finally:
        container_pool.append(container)


def container_collection(container: list):
    while len(container) > 0:
        db_conn.insert_tweet(container.pop())
    db_conn.conn.commit()


def collection_process(dates_list: list):
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

target_dates = sorted([DATE_START + datetime.timedelta(days=i)
                       for i in range((DATE_END-DATE_START).days)],
                      reverse=True)
collection_process(target_dates)

for _ in range(MISSING_DATES_TRIAL_COUNT):
    missing_dates = get_missing_dates(reverse_sorted=True)
    print(f"Number of missing days: {len(missing_dates)}")

    if not len(missing_dates):
        break

    collection_process(missing_dates)

print(f"Collector finished in {datetime.timedelta(seconds=time.time() - t0)}")
