import pandas as pd
import re
from nltk.tokenize import word_tokenize
import os
from lemmatizer import word_lemmatizer


class PreprocessNewsData:
    def __init__(self):
        self.df_news = pd.DataFrame()
        self.news = pd.read_json('data/newsgroup.json')
        
        print('***** Filtering columns *****')
        self.create_subject()
        print('***** Cleaning Data *****')
        self.clean_data()
        print('***** Tokenizing Data *****')
        self.tokenize()

        print('***** Loading Lemmatized Data *****')
        lemmatized_data_path = 'data/lemmatized_df.csv'
        columns = self.df_news.columns
        if os.path.exists(lemmatized_data_path):
            self.df_lemmatized = pd.read_csv(lemmatized_data_path)
        else:
            # run only on GPU
            self.df_lemmatized = word_lemmatizer(self.df_news['tokenized_words'])
            self.df_lemmatized.to_csv(lemmatized_data_path, index=False)

        try:
            self.df_news.insert(loc=len(columns),column='clean_keywords', value=self.df_lemmatized['final_keywords'].tolist())
        except:
            self.df_news.drop(self.df_news.index[100], inplace=True)
            self.df_news.insert(loc=len(columns),column='clean_keywords', value=self.df_lemmatized['final_keywords'].tolist())

    def create_subject(self):
        # create subject column
        for idx, txt in enumerate(self.news['content']):
            subject = re.findall('Subject:(.*\n)', txt)
            if len(subject) > 0:
                self.news.loc[idx, 'subject'] = str(idx) + ' ' + subject[0]
            else:
                self.news.loc[idx, 'subject'] = 'NA'

        self.df_news = self.news[['subject', 'content']]

    def clean_data(self):
        # change to a lower case
        self.df_news.loc[:,'content'] = self.df_news.loc[:, 'content'].str.lower()
        # self.df_news.loc[:,'subject'] = self.df_news.loc[:, 'subject'].str.lower()
        SW = ['subject:', 'organization:', 'thanks', 'thank', 're:']
        for sw in SW:
            self.df_news.loc[:,'content'] = self.df_news.loc[:, 'content'].str.replace(sw, '')

        # DATA CLEANING
        # ----- CONTENT -----
        # remove from to email
        self.df_news.content.replace(to_replace='from:(.*\n)',value= '', regex=True, inplace=True)
        self.df_news.content.replace(to_replace='lines:(.*\n)', value='', regex=True, inplace=True)
        # remove punctuations
        self.df_news.content.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]', value=' ', regex=True, inplace=True)
        self.df_news.content.replace(to_replace='-', value=' ', regex=True, inplace=True)
        self.df_news.content.replace('\s+', ' ',regex=True, inplace=True)
        # remove double white space
        self.df_news.content.replace('  ', '', regex=True, inplace=True)
        # remove single white space
        self.df_news.loc[:, 'content'] = self.df_news.loc[:, 'content'].apply(lambda x: x.strip())

        # ----- SUBJECT -----
        self.df_news.subject.replace('Re:', '', regex=True, inplace=True)
        self.df_news.subject.replace('[!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]', ' ', regex=True, inplace=True)
        self.df_news.subject.replace('\s+', ' ',regex=True, inplace=True)
        self.df_news.subject.replace('  ', '', regex=True, inplace=True)
        self.df_news.loc[:, 'subject'] = self.df_news.loc[:, 'subject'].apply(lambda x: x.strip())

    def tokenize(self):
        tokenized_words = [word_tokenize(entry) for entry in self.df_news.content]
        self.df_news.loc[:, 'tokenized_words'] = tokenized_words
