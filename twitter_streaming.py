import tweepy
from NER import NER
from NLG import MRK_NLG

#Variables that contains the user credentials to access Twitter API (Tweet extraction)
access_key = "1119680381479989248-H48YpATLs7DZvU9Zj7Xq0LS1hHh1QQ"
access_secret = "eFHOQxq6SPAXDcmzdCkFqDc0Jmzuzu9Tttk1iVxuZKBYf"
consumer_key = "f6x7T0Q2jKealjDIPaYK4wUTD"
consumer_secret = "jacs6wq0OyvPQneTnJ0RqfAtNDQoCEE6UJ8iLSJC2GaajZ2Ctk"

#Variables that contains the user credentials to access Twitter API (Tweet posting)
access_key_2        = "1119680381479989248-H48YpATLs7DZvU9Zj7Xq0LS1hHh1QQ"
access_secret_2     = "eFHOQxq6SPAXDcmzdCkFqDc0Jmzuzu9Tttk1iVxuZKBYf"
consumer_key_2      = "f6x7T0Q2jKealjDIPaYK4wUTD"
consumer_secret_2   = "jacs6wq0OyvPQneTnJ0RqfAtNDQoCEE6UJ8iLSJC2GaajZ2Ctk"

# Function to login and set API object with username global data
def login(username):
    global user_first_name
    global user_location
    # Authorization to consumer key and consumer secret
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Access to user's access key and access secret
    auth.set_access_token(access_key, access_secret)

    # Calling api
    api = tweepy.API(auth)

    user = api.get_user(id=username)
    user_first_name = (user.name).split(" ")[0]
    user_location = user.location

    return api


# Function to extract tweets
def get_tweets(api, username, number_of_tweets):
    # Empty Array
    tweets_list = []

    # create array of tweet information: username,
    # tweet id, date/time, text
    #tweets_for_csv = [tweet.text for tweet in tweets]  # CSV file created
    tweets = api.user_timeline(id=username, count=number_of_tweets, tweet_mode='extended')
    for tweet in tweets:
        # Appending tweets to the empty array tmp
        tweets_list.append(tweet.full_text)

    # Printing the tweets
    print(tweets_list)
    return tweets_list


def create_phishing_msg(work_of_art, countries, hobbies):
    global user_first_name
    global user_location
    if user_location == "":
        print(countries)
        user_location = max(set(countries), key=countries.count)

    print("\n\n\n***** Phishing Message *****\n" + "User First Name = " + user_first_name + ", User Location = " + user_location + ", User Hobbies = " + ",".join(hobbies) + ", User Favorite Work of Art = " + ",".join(work_of_art))
    print("\n***** Phishing Message *****\n\n")

    #msg = "\n\nHi " + user_first_name + "!\nI would like to invite you to a competition in " + user_location
    msg_types = []
    msg_types.append("Hi " + user_first_name + "!" + \
           "\nThere's a new award winning competition at " + user_location + " which will include " + ", ".join(hobbies) + \
           "\nEverybody is welcomed <URL>")
    msg_types.append("Hi everybody!" + \
          "\nThere's a new award winning competition at " + user_location + " which will include " + ", ".join(hobbies) + \
          "\nEverybody is welcomed <URL>")

    msg_types.append("Hi everybody!" + \
           "\nWe opened a new theater in " + user_location + " showing " + ", ".join(work_of_art) + \
           "\nFREE tickets here <URL>")
    msg_types.append("Hi " + user_first_name + "!" +
            "\nWe opened a new theater in " + user_location + " showing " + ", ".join(work_of_art) + \
            "\nFREE tickets here <URL>")

    for idx, msg in enumerate(msg_types):
        print("Msg format " + str(idx) + ":\n" + str(msg))

    return msg_types[2]

def post_tweet(api, tweet):
    if tweet is not None:
        api.update_status(status=tweet)
        print("Tweet: " + str(tweet) + " Posted.")


if __name__ == '__main__':
    # Properties
    process_again = False
    auto_post = True
    man_select_tweet = False
    user_name = "badbanana"
    # 200 tweets to be extracted
    number_of_tweets = 200

    # Here goes the twitter handle for the user
    # whose tweets are to be extracted.
    ner = NER()

    # Data retrieval and NER processing
    api = login(user_name)
    if process_again:
        tweets = get_tweets(api, user_name, number_of_tweets)
        print("****** NLTK STANFORD NER ******")
        for i, tweet in enumerate(tweets):
            print("Tweet number: " + str(i) + " Out of " + str(len(tweets)))
            ner.nltk_stanford_ner(tweet)

        print("****** SPACY ******")
        for i, tweet in enumerate(tweets):
            print("Tweet number: " + str(i) + " Out of " + str(len(tweets)))
            ner.preprocess_spacy(tweet)

        # Remove duplications
        ner.remove_dup()

        ner.dump_json('data.txt')
    else:
        ner.load_json('data.txt')
        print("Loaded : " + str(len(ner.loaded_data)))

    ner.create_tweets_list()
    ner.create_word_list()
    print(ner.work_of_art)
    print(ner.countries)
    print(ner.hobbies)

    selected_tweet = None
    m_nlg = MRK_NLG(ner.all_tweets)
    for i in range(100):
        is_a_tweet = str(m_nlg.create_tweet())
        if is_a_tweet is not None:
            selected_tweet = is_a_tweet

    phishing_msg = create_phishing_msg(ner.work_of_art, ner.countries, ner.hobbies)

    if auto_post is True:
        if man_select_tweet is True:
            selected_tweet = raw_input("Please enter the wanted tweet (you can use the output above)")
        post_tweet(api, phishing_msg)