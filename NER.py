import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.tag import StanfordNERTagger
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
import spacy
import os
from spacy import displacy
from collections import Counter


class NER:

    def __init__(self):
        java_path = "C:/Program Files/Java/jdk1.8.0_201/bin/java.exe"
        os.environ['JAVAHOME'] = java_path
        nltk.download('punkt')
        nltk.download('averaged_perceptron_tagger')
        self.stanford_ner_tagger = StanfordNERTagger(
            'stanford-ner-2018-10-16/classifiers/english.all.3class.distsim.crf.ser.gz',
            'stanford-ner-2018-10-16/stanford-ner-3.9.2.jar'
        )
        self.spacy_nlp = spacy.load('en_core_web_sm')

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
        print ("\nOriginal post: %s", post)
        for result in results:
            tag_value = result[0]
            tag_type = result[1]
            if tag_type != 'O':
                print('Type: %s, Value: %s' % (tag_type, tag_value))

    def preprocess_spacy(self, post):
        print("\nOriginal post: %s", post)
        results = self.spacy_nlp(post)
        for element in results.ents:
            print('Type: %s, Value: %s' % (element.label_, element))
