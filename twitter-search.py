#!/usr/bin/env python

import json
import config
from twitter import *
from json import dumps

import sys
sys.path.append(".")

twitter = Twitter(auth=OAuth(config.access_key,
                             config.access_secret,
                             config.consumer_key,
                             config.consumer_secret))

useOutname = False
useQuery = False
outname = "tweets.json"
queryTerm = ""
for argument in sys.argv:
    if useOutname:
        useOutname = False
        outname = argument
    elif argument == "--outname":
        useOutname = True
    elif useQuery:
        useQuery = False
        queryTerm = argument
    elif argument == "--query":
        useQuery = True

if queryTerm == "":
    print("Please provide a query using the flag --query")
    exit(-1)

read_texts = {}
query = twitter.search.tweets(q=queryTerm, lang="en", count="100")
for repeat in range(0, 20):
    with open(outname, "a") as file:
        last_id = 0
        for tweet in query["statuses"]:
            if not tweet["text"] in read_texts and "created_at" in tweet:
                read_texts[tweet["text"]] = tweet["id"]
                last_id = tweet["id"]
                reduced_tweet = {key: tweet[key]
                                 for key in ["id", "text"]}
                file.write(dumps(reduced_tweet) + "\n")
    if last_id == 0:
        print("ran out of tweets")
        break
    query = twitter.search.tweets(
        q=queryTerm, lang="en", count="100", max_id=last_id)
print("\nWrote ", outname, " to current directory")
