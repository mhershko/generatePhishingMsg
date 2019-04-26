import json
from django.conf import settings
from django.http import HttpResponse
import facebook
import requests
import pickle
import time
import random
import pandas as pd
import string
import nltk

app_id = "2310735412324019"
app_secret = "ba377ec43ccabf958d5eafa77930ac70"
access_token = 'EAAg1mgNr5rMBABrx6sG1yTsFCvqv2rs5KgOyc10sDUmsKmTiu3b2RoJYea8hAJi6UZAmW0wymvdmFAY3IbBbP5IAeuxNrJm5SQccLuFgfVzwj35st11zNAiChNij5SVgTG854Vaypxr00KpRmNi6eRcOqqjQZD'


class FacebookFeed:

    def get_profile(cls, user_id, count=6):
        try:
            graph = facebook.GraphAPI(access_token)
            profile = graph.get_object('me', fields="posts")
            print profile
            return profile
        except facebook.GraphAPIError:
            print facebook.GraphAPIError.message

def save_posts(profile):
    http_res = HttpResponse(json.dumps(profile), content_type="application/json")
    data = profile['posts']['data']
    print data
    pickle.dump(data, open("steam_data.pkl", "wb"))
    return data


def clean_data(data):
    loaded_data = pickle.load(file=open("steam_data.pkl"))
    df = pd.io.json.json_normalize(data=loaded_data)
    print df
    return df


def count_words(df):
    # FixMe - fix stop_words list
    stop_words = set(nltk.corpus.stopwords.words('english'))
    words_dic = {}
    mapping = dict.fromkeys(map(ord, string.punctuation))
    for message in df['message']:
        try:
            words = message.split(' ')
            for word in words:
                word = word.strip()
                word = word.lower()
                # remove punctuation marks
                word = word.translate(mapping)
                if word in stop_words:
                    continue
                if word in words_dic:
                    words_dic[word] += 1
                else:
                    words_dic[word] = 1
        except AttributeError:
            pass

    return words_dic


if __name__ == '__main__':
    user_feed = FacebookFeed().get_profile(user_id="100004231413769")
    if not user_feed:
        http_res = HttpResponse(status=500, content="Can't get posts for user", content_type="application/json")

    else:
        data = save_posts(user_feed)
        # normalize and clean data
        posts_df = clean_data(data)
        # count top words
        words = count_words(posts_df)
        top_words_df = pd.DataFrame(words.items(), columns=['Word', 'Count'])
        top_words_df.sort_values('Count', ascending=False, inplace=True)
        print top_words_df


