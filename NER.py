import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import spacy
import os
from textblob import TextBlob
from spacy import displacy
from collections import Counter
import json
import re


class NER:

    def __init__(self):
        #java_path = "C:/Program Files/Java/jdk1.8.0_101/bin/java.exe"
        java_path = "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
        os.environ['JAVAHOME'] = java_path
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        self.stanford_ner_tagger = StanfordNERTagger(
            'stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
            'stanford-ner-2018-10-16/stanford-ner-3.9.2.jar'
        )
        with open('hobbies.txt', 'r') as f:
            self.list_of_hobbies = [line.lower().strip() for line in f]

        self.spacy_nlp = spacy.load('en_core_web_sm')
        self.data = []
        self.loaded_data = {}
        self.out_words = []
        self.all_tweets = []
        self.work_of_art = []
        self.countries = []
        self.hobbies = []

    def clean_tweet(self, tweet):
        """
        The formatting regex is stolen wholesale from twilio's great blog post:
        https://www.twilio.com/blog/2016/09/fun-with-markov-chains-python-and-twilio-sms.html
        The fish names are all my fault.
        """
        tweet = re.sub("https?\:\/\/", "", tweet)  # links
        tweet = re.sub("t.co\/([a-zA-Z0-9]+)", "", tweet)
        tweet = re.sub("bit.ly\/([a-zA-Z1-9]+)", "", tweet)
        tweet = re.sub("Video\:", "", tweet)  # Videos
        tweet = re.sub("\n", " ", tweet)  # new lines
        tweet = re.sub("\s+", " ", tweet)  # extra whitespace
        tweet = re.sub("&amp;", "and", tweet)  # encoded ampersands
        # now the silliness begins.
        tweet = re.sub("[H*h*]illary", "Halibut", tweet)
        tweet = re.sub("[F*f*]lynn", "Fish", tweet)
        tweet = re.sub("[S*s*]calia", "Scallop", tweet)
        tweet = re.sub("[P*p*]ence", "Perch", tweet)
        tweet = re.sub("[S*s*]anders", "Sardine", tweet)
        tweet = re.sub("[O*o*]bama", "Otter", tweet)
        tweet = re.sub("[M*m*]elania", "Mackeral", tweet)
        tweet = re.sub("[M*m*]attis", "Mahi-mahi", tweet)
        tweet = re.sub("[T*t*]illerson", "Tilapia", tweet)
        tweet = re.sub("[P*p*]odesta", "Pufferfish", tweet)
        tweet = re.sub("[P*p*]utin", "Piranha", tweet)
        tweet = re.sub("[K*k*]elly", "Keelfish", tweet)
        tweet = re.sub("[S*s*]ean", "Suckerfish", tweet)
        tweet = re.sub("[O*o*](')?[R*r*]eilly", "ORoughy", tweet)
        tweet = re.sub("[O*o*]bama\s?[C*c*]are", "OtterCare", tweet)
        tweet = re.sub("[S*s*]essions", "Shrimpfish", tweet)
        tweet = re.sub("[K*k*]aine", "Kelp", tweet)
        tweet = re.sub("[W*w*]arren", "Walleye", tweet)
        tweet = re.sub("[I*i*]slam(ic)?", "Orca", tweet)
        tweet = re.sub("ISIS", "OSIS", tweet)
        tweet = re.sub("[M*m*]uslim", "Orca", tweet)
        tweet = re.sub("Ted ", "Tetra ", tweet)
        tweet = re.sub("@realdonaldtrump", "@sealdonaldtrump", tweet)
        return tweet

    def process_post(self, post):
        post = str(post)
        print("\nOriginal post: %s", post)
        c_post = self.clean_tweet(post)
        print("\nClean post: %s", c_post)
        self.data.append({
            'post': post,
            'c_post': c_post,
            'words': [],
        })

    def process_element(self, cat, value):
        cat = str(cat).strip()
        value = str(value).strip()
        print('Type: %s, Value: %s' % (cat, value))
        self.data[len(self.data) - 1]['words'].append({
            cat : value,
        })
        if cat == 'WORK_OF_ART':
            self.work_of_art.append(value)
        if cat == 'GPE' or 'LOCATION':
            self.countries.append(value)
        if value in self.list_of_hobbies:
            self.hobbies.append(value)

    # preprocess data using nltk library
    def preprocess_nltk(self, post):
        # apply word tokenization and part-of-speech tagging
        post = nltk.word_tokenize(post)
        post = nltk.pos_tag(post)
        # return post
        # implement noun phrase chunking to identify named entities using a regular expression consisting of rules that indicate how sentences should be chunked
        pattern = 'NP: {<DT>?<JJ>*<NN>}'
        # create a chunk parser
        cp = nltk.RegexpParser(pattern)
        cs = cp.parse(post)
        print(cp)
        # represent chunk structures with IOB tags
        iob_tagged = tree2conlltags(cs)
        pprint(iob_tagged)
        # recognize named entities using a classifier
        ne_tree = nltk.ne_chunk(pos_tag(word_tokenize(post)))
        print(ne_tree)

    def nltk_stanford_ner(self, post):
        results = self.stanford_ner_tagger.tag(post.split())
        self.process_post(post)
        for result in results:
            tag_value = result[0]
            tag_type = result[1]
            if tag_type != 'O':
                self.process_element(tag_type, tag_value)
            if tag_value in self.list_of_hobbies:
                self.hobbies.append(tag_value)

    def preprocess_spacy(self, post):
        self.process_post(post)
        results = self.spacy_nlp(post)
        for element in results.ents:
            self.process_element(element.label_, element.string)

    def preprocess_textblob(self, post):
        self.process_post(post)
        blob = TextBlob(post)
        for element in blob.tags:
            self.process_element(element.label_, element)

    def dump_json(self, file_name):
        with open(file_name, 'w') as outfile:
            json.dump(self.data, outfile)

    def load_json(self, file_name):
        with open(file_name) as json_file:
            self.loaded_data = json.load(json_file)

    def create_tweets_list(self):
        for t in self.data:
            self.all_tweets.append(t['c_post'])

        for t in self.loaded_data:
            self.all_tweets.append(t['c_post'])


    def create_word_list(self):
        for t in self.data:
            for w in t["words"]:
                self.out_words.append(w)

        for t in self.loaded_data:
            for w in t["words"]:
                for key, value in w.items():
                    self.out_words.append(value)