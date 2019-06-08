import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import markovify #Markov Chain Generator

class MRK_NLG:
    def __init__(self, list):
        self.text = " ".join(list)
        self.text_model = markovify.Text(self.text, state_size=2)

    def create_tweet(self):
        # text_model = markovify.NewlineText(self.dict, state_size=2)
        print(self.text_model.make_short_sentence(140))
