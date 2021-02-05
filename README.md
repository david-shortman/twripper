# Twitter List Scraper

## Prepare your environment

Create a virtual environment using `virtualenv env` and then activate that environment using `source venv/bin/activate`

Install the requirements for the script by running `pip install -r requirements.txt`

Download the corpora for the sentiment analysis using the command `python -m textblob.download_corpora`

Create a file named config.py with the following contents (replacing the context between the <> symbols with your Twitter keys):

`consumer_key = "<CONSUMER_KEY>"
consumer_secret = "<CONSUMER_SECRET>"
access_key = "<ACCESS_KEY>"
access_secret = "<ACCESS_SECRET>"`

## Running the script

After finding a Twitter list you would like to load tweets from, run the following command:

`python twitter-list-scraper.py --outname <OUTNAME> --sources <SOURCES>`

`<OUTNAME>` is the desired name of the output JSON file, and `<SOURCES>` is a space-separated list of Twitter list objects. Twitter list objects are written as the following: `<LIST_NAME>,<LIST_AUTHOR>,<LEAN>`.

Example command:

`python twitter-list-scraper.py --outname tweets.json --sources conservative-voices,bponsot,right liberals,mattklewis,left`

## Output

The output file consists of JSON formatted tweets, separated by newlines. Each tweet contains an id, text, sentiment and subjectivity ratings, and the prescribed lean.

Sample tweet:

```
{
    "id": 1118129766413033472,
    "text": "Majority of Republicans think evangelical Christians are more discriminated against than minorities\u2026 https://t.co/PeJSEoc2Ea",
    "softSentiment": "positive",
    "mediumSentiment": "positive",
    "harshSentiment": "neutral",
    "softSubjectivity": "subjective",
    "mediumSubjectivity": "subjective",
    "harshSubjectivity": "objective",
    "lean": "left"
}