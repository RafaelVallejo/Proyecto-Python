

class AccountStatistics(object):

    def __init__(self):
        self.used_hashtags = 0
        self.tweets_for_day = {}
        self.hour_of_max_activity = ''
        self.number_of_tweets_to_other_site = 0
        self.list_of_tweets_to_other_site = []
        self.tweets_geolocalizados  = 0
        self.list_of_tweets_geolocalizados = []
        self.tweets_with_device_info = 0
        self.list_of_tweets_device_info = []
        self.tweets_generated_other_accounts = 0
        self.list_tweets_generated_other_accounts = []
        self.tweets_mention_accout = 0
        self.list_tweets_mention_accout = []
        self.analized_tweets_url = {}
        self.content_multimedia_tweets_url = []




class Tweet(objetc):

    def __init__(self,date,fragment,url):
        self.date = date
        self.fragment = fragment
        self.url = url

    def __str__(self):
        return '%s   %s   %s '%(self.date, self.fragment ,self.url)
