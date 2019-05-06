import requests as r
import json
import time
import csv

#===================================================================================

class redditArchiver:
    # url = "https://api.pushshift.io/reddit/search/submission?is_self=true&size=1000&author!=[deleted]&subreddit=%s&after=%i&before=%i"
    # the base pushshift url that we will use to get data
    URL = "https://api.pushshift.io/reddit/search/submission?"

    def __init__(self):
