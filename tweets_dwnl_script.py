import json
import time
from TwitterAPI import TwitterAPI
from TwitterAPI import TwitterConnectionError


consumer_key = "your_consumer_key"
consumer_secret = "your_consumer_secret_key"
access_token_key = "your_access_token"
access_token_secret = "your_token_secret"

# This is the object that we will use to send the request to Twitter
# A request is a HTTP request, just like your browser does when it goes to a website!
api = TwitterAPI(consumer_key, consumer_secret, access_token_key,
                 access_token_secret)


def get_tweets(base_outfile, kwrd):
    file_num = 1
    num_lines = 0
    num_retries = 0

    # This asks twitter to open up a stream of data
    # The stream sends tweets that come from the specified location.
    while True:
        try:
            outfile = "{0}{1}.json".format(base_outfile, file_num)
            f = open(outfile, "w")
            r = api.request('statuses/filter', {'track': kwrd})
            num_retries = 0
            for tweet in r:
                try:
                    data = json.dumps(tweet)
                    print(tweet["text"])
                    f.write("{0}\n".format(data))
                except:
                    pass
                else:
                    num_lines += 1
                    if not num_lines % 1000000:
                        file_num += 1
                        f.close()
                        outfile = "{0}{1}.json".format(base_outfile, file_num)
                        f = open(outfile, "w")
        except TwitterConnectionError:
            num_retries += 1
            time.sleep(num_retries)
    file_num += 1


get_tweets('your_folder_location', 'your search keywords (space = AND, comma = OR)')


