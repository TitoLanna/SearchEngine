import pandas as pd
from nltk.tokenize import word_tokenize
from lemmatizer import word_lemmatizer


class PreprocessLyricsData:
    def __init__(self):
        self.df_lyrics = pd.DataFrame()
        self.lyrics = pd.read_json('data/lyrics.json')
        
        print('***** Filtering columns *****')
        self.create_subject()
        print('***** Cleaning Data *****')
        self.clean_data()
        print('***** Tokenizing Data *****')
        self.tokenize()

        print('***** Loading Lemmatized Data *****')
        columns = self.df_lyrics.columns
        self.df_lemmatized = word_lemmatizer(self.df_lyrics['tokenized_words'])
        try:
            self.df_lyrics.insert(loc=len(columns),column='clean_keywords', value=self.df_lemmatized['final_keywords'].tolist())
        except:
            self.df_lyrics.drop(self.df_lyrics.index[100], inplace=True)
            self.df_lyrics.insert(loc=len(columns),column='clean_keywords', value=self.df_lemmatized['final_keywords'].tolist())

    def create_subject(self):
        # create subject column
        for idx, txt in enumerate(self.lyrics['file_name']):
            self.lyrics.loc[idx, 'subject'] = str(idx) + ' ' + txt
            
        self.df_lyrics = self.lyrics[['subject', 'content']]

    def clean_data(self):
        # change to a lower case
        self.df_lyrics.loc[:,'content'] = self.df_lyrics.loc[:, 'content'].str.lower()
        # self.df_news.loc[:,'subject'] = self.df_news.loc[:, 'subject'].str.lower()

        # DATA CLEANING
        # ----- CONTENT -----
        # remove punctuations
        self.df_lyrics.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', value=' ', regex=True, inplace=True)
        self.df_lyrics.content.replace(to_replace='-', value=' ', regex=True, inplace=True)
        self.df_lyrics.content.replace('\s+', ' ',regex=True, inplace=True)
        # remove double white space
        self.df_lyrics.content.replace('  ', '', regex=True, inplace=True)
        # remove single white space
        self.df_lyrics.loc[:, 'content'] = self.df_lyrics.loc[:, 'content'].apply(lambda x: x.strip())

        # ----- SUBJECT -----
        self.df_lyrics.loc[:, 'subject'] = self.df_lyrics.loc[:, 'subject'].apply(lambda x: x.strip())

    def tokenize(self):
        tokenized_words = [word_tokenize(entry) for entry in self.df_lyrics.content]
        self.df_lyrics.loc[:, 'tokenized_words'] = tokenized_words
