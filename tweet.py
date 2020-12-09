import time


class Tweet:

    def __init__(self, **kwargs):
        """
            Tweet instance that keeps information of a tweet. To create an
            instance some keyword arguments must be set.

                Args:
                    `tweet_id` (int): id number of tweet
                    `writer` (str): id of owner of the tweet
                    `post_date` (struct time): struct time of tweet's post date
                    `body` (str): content of tweet
                    `searchKey` (str)(optional): search key that tweet is found
                    `comment_num` (int)(optional): number of comments of tweet
                    `retweet_num` (int)(optional): number of retweets of tweet
                    `like_num` (int)(optional): number of likes of tweet

                Raises:
                    TypeError if `post_date` argument is not `struct_time`
        """
        if not isinstance(kwargs['post_date'], time.struct_time):
            raise TypeError("expected:{} but found: {}".format(
                time.struct_time, type(kwargs['post_date'])))

        self.tweet_id = kwargs['tweet_id']
        self.writer = kwargs['writer']
        self.post_date = kwargs['post_date']
        self.body = kwargs['body']
        try:
            self.searchKey = kwargs['searchKey']
        except KeyError:
            self.searchKey = None
        try:
            self.comment_num = kwargs['comment_num']
        except KeyError:
            self.comment_num = None
        try:
            self.retweet_num = kwargs['retweet_num']
        except KeyError:
            self.retweet_num = None
        try:
            self.like_num = kwargs['like_num']
        except KeyError:
            self.like_num = None

    def __hash__(self):
        return self.tweet_id

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.tweet_id == other.tweet_id

    def __str__(self):
        s1 = f"writer: {self.writer}, date: {time.strftime('%Y-%m-%d_%H:%M:%S', self.post_date)}"
        s2 = f"\n{self.body}\n"
        s3 = f"comment: {self.comment_num}\tretweet: {self.retweet_num}\tlike: {self.like_num}"
        return s1 + s2 + s3 + '\n\n'
