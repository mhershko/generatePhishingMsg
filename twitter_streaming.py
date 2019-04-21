import tweepy
import facebook

#Variables that contains the user credentials to access Twitter API
access_key = "1119680381479989248-H48YpATLs7DZvU9Zj7Xq0LS1hHh1QQ"
access_secret = "eFHOQxq6SPAXDcmzdCkFqDc0Jmzuzu9Tttk1iVxuZKBYf"
consumer_key = "f6x7T0Q2jKealjDIPaYK4wUTD"
consumer_secret = "jacs6wq0OyvPQneTnJ0RqfAtNDQoCEE6UJ8iLSJC2GaajZ2Ctk"


# Function to extract tweets
def get_tweets(username):
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)

    # 200 tweets to be extracted
    number_of_tweets = 200
    tweets = api.user_timeline(id="realDonaldTrump")

    # Empty Array
    tmp = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    #tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    for tweet in tweets:
        # Appending tweets to the empty array tmp
        tmp.append(tweet.text)

        # Printing the tweets
    print(tmp)


def get_facebook_posts():
    user_long_token = 'EAAg1mgNr5rMBABrx6sG1yTsFCvqv2rs5KgOyc10sDUmsKmTiu3b2RoJYea8hAJi6UZAmW0wymvdmFAY3IbBbP5IAeuxNrJm5SQccLuFgfVzwj35st11zNAiChNij5SVgTG854Vaypxr00KpRmNi6eRcOqqjQZD'
    graph = facebook.GraphAPI(access_token=user_long_token, version="2.7")

# Driver code
if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    get_tweets("twitter-handle")