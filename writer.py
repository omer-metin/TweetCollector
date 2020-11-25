import time


class Writer:

    def __init__(self, **kwargs):
        """
            writer instance that keeps infromation of twitter user.
            To create an instance some keyword arguments must be set.

                Args:
                    `user_id` (str): id of twitter user
                    `username` (str): name of twitter user
                    `following` (int): following count of user
                    `follower` (int): follower count of user
                    `tweet_count` (int): tweet count of user
                    `bio_text` (text): bio text of user
                    `location` (text): location information of user
                    `website` (str): website information of user
                    `born` (struct_time): birth date of user in struct_time
                    `joined` (struct_time): join date of user to twitter in struct_time
        """

        self.user_id = kwargs['user_id']
        self.username = kwargs['username']
        self.following = kwargs['following']
        self.follower = kwargs['follower']
        try:
            self.tweet_count = kwargs['tweet_count']
        except KeyError:
            self.tweet_count = None
        try:
            self.bio_text = kwargs['bio_text']
        except KeyError:
            self.bio_text = None
        try:
            self.location = kwargs['location']
        except KeyError:
            self.location = None
        try:
            self.website = kwargs['website']
        except KeyError:
            self.website = None
        try:
            self.born = kwargs['born']
            if not isinstance(self.born, time.struct_time):
                if self.born is not None:
                    print("Born must be struct_time")
                    self.born = None
        except KeyError:
            self.joined = None
        try:
            self.joined = kwargs['joined']
            if not isinstance(self.joined, time.struct_time):
                print("Joined time must be struct_time")
                self.joined = None
        except KeyError:
            self.joined = None

    def __hash__(self):
        return self.user_id

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.user_id == other.user_id
