import tweepy
from NER import NER
from NLG import MRK_NLG

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
    tweets = api.user_timeline(id=username, count = number_of_tweets, tweet_mode = 'extended')

    # Empty Array
    tweets_list = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    #tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    for tweet in tweets:
        # Appending tweets to the empty array tmp
        tweets_list.append(tweet.full_text)

    # Printing the tweets
    print(tweets_list)
    return tweets_list


if __name__ == '__main__':
    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    ner = NER()

    # Data retrieval and NER processing
    process_again = True
    if process_again:
        tweets = get_tweets("realDonaldTrump")
        print("****** NLTK STANFORD NER ******")
        for tweet in tweets:
           ner.nltk_stanford_ner(tweet)
        ner.dump_json('stanford.txt')
        print("****** SPACY ******")
        for tweet in tweets:
            ner.preprocess_spacy(tweet)
        ner.dump_json('spacy.txt')
    else:
        ner.load_json('stanford.txt')
        #ner.load_json('spacy.txt')
        print("Loaded : " + str(len(ner.loaded_data)))

    ner.create_tweets_list()
    ner.create_word_list()

    m_nlg = MRK_NLG(ner.all_tweets)
    for i in range(100):
        m_nlg.create_tweet()