import sqlite3
import time
from datetime import datetime

from tweet import Tweet
from writer import Writer


class TweetDB:

    def __init__(self, stock_market_name):
        """
            Database class for Tweets that will be collected. Uses SQLite3.

                Args:
                    `stock_market_name` (str): stock market name that will be
                        used as database name after creation there will be a 
                        .db file with this name in the directory

            To make database creation on memory set stock_market_name to `':memory:'`
        """
        self.name = stock_market_name + '.db' if stock_market_name != ':memory:' else ''
        self.conn = sqlite3.connect(f'{self.name}')
        self.c = self.conn.cursor()

    def create_tables(self):
        """Creates needed tables if they does not exists. """
        with self.conn:
            self.c.execute(
                """
                    CREATE TABLE IF NOT EXISTS Tweet (
                        tweet_id        INTEGER     PRIMARY KEY,
                        writer          TEXT        NOT NULL,
                        post_date       INTEGER     NOT NULL,
                        body            TEXT        NOT NULL,
                        comment_num     INTEGER,    
                        retweet_num     INTEGER,    
                        like_num        INTEGER
                    )
                """
            )
            # Create index on post_date
            self.c.execute(
                "CREATE INDEX IF NOT EXISTS IX_post_date ON Tweet (post_date);")
            # Create index on writer
            self.c.execute(
                "CREATE INDEX IF NOT EXISTS IX_writer ON Tweet (writer);")
            self.c.execute(
                """
                    CREATE TABLE IF NOT EXISTS Writer (
                        user_id         TEXT        PRIMARY KEY,
                        username        TEXT        NOT NULL,
                        following       INTEGER     NOT NULL,
                        followerer      INTEGER     NOT NULL,
                        tweet_count     INTEGER,
                        bio_text        TEXT,
                        location        TEXT,
                        website         TEXT,
                        birthdate       INTEGER,
                        joined          INTEGER
                    )
                """
            )
            self.c.execute(
                """
                    CREATE TABLE IF NOT EXISTS SearchKey_Tweet (
                        tweet_id        INTEGER,
                        searchKey       TEXT,
                        PRIMARY KEY (tweet_id, searchKey)
                    )
                """
            )

    def _insert_writer_executer(self, writer: Writer) -> None:
        """
            Executes a insert operation on single writer.
            Commit is needed after execution.

                Args:
                    `writer` (Writer): Writer instance to insert
        """
        try:
            self.c.execute(
                """
                    INSERT INTO Writer VALUES (
                        :user_id,
                        :username,
                        :following,
                        :follower,
                        :tweet_count,
                        :bio_text,
                        :location,
                        :website,
                        :birthdate,
                        :joined
                    )
                """,
                {
                    'user_id': writer.user_id,
                    'username': writer.username,
                    'following': writer.following,
                    'follower': writer.follower,
                    'tweet_count': writer.tweet_count,
                    'bio_text': writer.bio_text,
                    'location': writer.location,
                    'website': writer.website,
                    'birthdate': self.struct_to_seconds(writer.born) if writer.born else None,
                    'joined': time.mktime(writer.joined)
                }
            )
        except sqlite3.IntegrityError:
            print(f"Existing writer: {writer.user_id}")

    def insert_writers(self, writers):
        """
            Insert multiple writers.

                Args:
                    writers (Iterable): Writer instances to insert

                Raises:
                    ValueError if one of the writers is not an instance
                    of Writer. In the case none of the writers will be
                    inserted
        """
        if any([not isinstance(e, Writer) for e in writers]):
            raise ValueError(Writer)
        with self.conn:
            for writer in writers:
                self._insert_writer_executer(writer)

    def _insert_tweet_executer(self, tweet: Tweet) -> None:
        """
            Executes a insert operation on single tweet.
            Commit is needed after execution.

                Args:
                    `tweet` (Tweet): Tweet instance to insert
        """
        try:
            self.c.execute(
                """
                    INSERT INTO Tweet VALUES (
                        :tweet_id,
                        :writer,
                        :post_date,
                        :body,
                        :comment_num,
                        :retweet_num,
                        :like_num
                    )
                """,
                {
                    'tweet_id': tweet.tweet_id,
                    'writer': tweet.writer,
                    'post_date': time.mktime(tweet.post_date),
                    'body': tweet.body,
                    'comment_num': tweet.comment_num,
                    'retweet_num': tweet.retweet_num,
                    'like_num': tweet.like_num
                }
            )
        except sqlite3.IntegrityError:
            print(f"Existing tweet: {tweet.tweet_id}")
        try:
            self.c.execute(
                """
                    INSERT INTO SearchKey_Tweet VALUES (
                        :tweet_id,
                        :searchKey
                    )
                """,
                {
                    'tweet_id': tweet.tweet_id,
                    'searchKey': tweet.searchKey
                }
            )
        except sqlite3.IntegrityError:
            print(
                f"Existing tweet-searchKey pair: {tweet.tweet_id}-{tweet.searchKey}")

    def insert_tweet(self, tweet: Tweet) -> None:
        """
            Inserts single tweet.

                Args:
                    `tweet` (Tweet): Tweet instance to insert

                Raises:
                    TypeError if input tweet is not a Tweet instance
        """
        if not isinstance(tweet, Tweet):
            raise TypeError(Tweet)
        with self.conn:
            self._insert_tweet_executer(tweet)

    def insert_tweets(self, tweets):
        """
            Inserts multiple tweets.  

                Args:
                    `tweets` (iterable): any iterable that contains Tweet

                Raises:
                    ValueError if input tweets contains at least one value that 
                    is not a Tweet instance. In the case, none of the tweets 
                    will be inserted. Be careful while choosing number of 
                    tweets that will be inserted at once.
        """
        if any([not isinstance(tweet, Tweet) for tweet in tweets]):
            raise ValueError(Tweet)
        with self.conn:
            for tweet in tweets:
                self.insert_tweet(tweet)

    def _get_tweets_by_query(self, query: str, searchKey: str) -> list:
        """
            Recieves tweets from database with given query.

                Args:
                    `query` (str): SQLite query that will be executed
                                   (e.g. `"SELECT * FROM Tweet"`)
                    `searchKey` (str): search key

                Returns:
                    A list that contains Tweet instances created from executed
                    `query`
        """
        self.c.execute(query)
        tweets = []
        for row in self.c.fetchall():
            tweets.append(Tweet(tweet_id=row[0],
                                writer=row[1],
                                post_date=time.localtime(row[2]),
                                body=row[3],
                                searchKey=searchKey,
                                comment_num=row[4],
                                retweet_num=row[5],
                                like_num=row[6]))

        return tweets

    def get_tweet(self, tweet_id, searchKey) -> Tweet:
        return self._get_tweets_by_query(
            f"SELECT * FROM Tweet WHERE tweet_id={tweet_id}", searchKey)[0]

    def get_searchKey_tweets(self, searchKey) -> list:
        return self._get_tweets_by_query(
            f"""
                SELECT * 
                FROM Tweet
                WHERE tweet_id=(
                    SELECT tweet_id
                    FROM SearchKey_Tweet
                    WHERE searchKey='{searchKey}'
                )
            """,
            searchKey
        )

    def get_searchKeys(self):
        self.c.execute("SELECT DISTINCT searchKey FROM SearchKey_Tweet")
        return self.c.fetchall()

    def get_companies_by_query(self, query):
        self.c.execute(query)
        return self.c.fetchall()

    @staticmethod
    def struct_to_seconds(time_struct: time.struct_time):
        epoch = datetime(1970, 1, 1)
        t = datetime(time_struct.tm_year, time_struct.tm_mon,
                     time_struct.tm_mday)
        return (t-epoch).days * 24 * 3600

    def close_DB(self):
        self.conn.close()
