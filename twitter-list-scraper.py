from twitter import TwitterStream, OAuth, TwitterResponse, Twitter
import config
from json import dumps
from time import time
import sys
from textblob import TextBlob
import re

auth = OAuth(config.access_key,
             config.access_secret,
             config.consumer_key,
             config.consumer_secret)
t = Twitter(auth=auth, secure=True)


def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\\w+:\\/\\/\\S+)|(RT)", " ", tweet).split())


def get_tweet_sentiment(tweet, intensity):
    ''' 
    Utility function to classify sentiment of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set polarity
    if analysis.sentiment.polarity > intensity:
        return 'positive'
    elif analysis.sentiment.polarity < (-1 * intensity):
        return 'negative'
    else:
        return 'neutral'


def get_tweet_subjectivity(tweet, intensity):
    ''' 
    Utility function to classify subjectivity of passed tweet 
    using textblob's sentiment method 
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set subjectivity
    if analysis.sentiment.subjectivity > intensity:
        return 'subjective'
    else:
        return 'objective'


useArgName = False
useOutname = False
outname = "tweets.json"
for argument in sys.argv:
    if useOutname:
        useOutname = False
        outname = argument
    elif argument == "--outname":
        useOutname = True
    elif argument == "--sources":
        useArgName = True
    elif useArgName:
        start = time()
        list_name, source_name, lean = argument.split(",")
        tweet_list = t.lists.show(
            slug=list_name, owner_screen_name=source_name)
        tweet_iter = t.lists.statuses(list_id=tweet_list["id"], count=200)
        read_ids = {}
        for repeat in range(0, 200):
            with open(outname, "a") as file:
                last_id = 0
                for tweet in tweet_iter:
                    if not tweet["id"] in read_ids and "created_at" in tweet:
                        read_ids[tweet["id"]] = tweet["id"]
                        last_id = tweet["id"]
                        tweet["softSentiment"] = get_tweet_sentiment(
                            tweet["text"], .01)
                        tweet["mediumSentiment"] = get_tweet_sentiment(
                            tweet["text"], .2)
                        tweet["harshSentiment"] = get_tweet_sentiment(
                            tweet["text"], .5)
                        tweet["softSubjectivity"] = get_tweet_subjectivity(
                            tweet["text"], .1)
                        tweet["mediumSubjectivity"] = get_tweet_subjectivity(
                            tweet["text"], .3)
                        tweet["harshSubjectivity"] = get_tweet_subjectivity(
                            tweet["text"], .6)
                        tweet["lean"] = lean
                        reduced_tweet = {key: tweet[key]
                                         for key in ["id", "text", "softSentiment", "mediumSentiment", "harshSentiment", "softSubjectivity", "mediumSubjectivity", "harshSubjectivity", "lean"]}
                        reduced_tweet["text"] = clean_tweet(tweet["text"])
                        file.write(dumps(reduced_tweet) + "\n")
                    print("read some tweet at ", str(time()),
                          "| elapsed time: ", str(time() - start))
                if last_id == 0:
                    print("ran out of tweets")
                    break
                tweet_iter = t.lists.statuses(
                    list_id=tweet_list["id"], count=200, max_id=last_id)
        print("\nWrote ", outname, " to current directory")