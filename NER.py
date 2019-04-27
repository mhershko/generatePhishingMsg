import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import spacy
from spacy import displacy
from collections import Counter
#import en_core_web_sm


class NER:

    def __init__(self):
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')

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

    def preprocess_spacy(self, post):
        post = spacy.nlp(post)
        pprint([(X.text, X.label_) for X in post.ents])
