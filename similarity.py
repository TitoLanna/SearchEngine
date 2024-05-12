import pandas as pd
import numpy as np
import re
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from lemmatizer import word_lemmatizer


class Similarity:
    def __init__(self, data):
        self.data = data
        self.__create_vocabulary()
    
    def __create_vocabulary(self):
        vocabulary = set()
        for doc in self.data.clean_keywords:
            vocabulary.update(doc.split(','))
        self.vocabulary = list(vocabulary)
    
    def __gen_vector_T(self, tokens):
        q_vocab = np.zeros((len(self.vocabulary)))
        x = self.tfidf.transform(tokens)
        for token in tokens[0].split(','):
            try:
                ind = self.vocabulary.index(token)
                q_vocab[ind] = x[0, self.tfidf.vocabulary_[token]]
            except:
                pass
        return q_vocab
    
    def __cosine_sim(self, a, b):
        cos_score = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
        return cos_score

    def cosine_similarity(self, k, query):
        if not query:
            return pd.DataFrame()
        self.k = k        
        self.query = query.lower()
        print('***** Calculating Similarity Score *****')
        self.tfidf = TfidfVectorizer(vocabulary=self.vocabulary, dtype=np.float32)
        self.tfidf.fit(self.data.clean_keywords)
        self.tfidf_tran = self.tfidf.transform(self.data.clean_keywords)
        # removes any non-word character (equivalent to `[^a-zA-Z0-9_]`)
        preprocessed_query = re.sub("\W+", " ", self.query).strip()
        tokens = word_tokenize(str(preprocessed_query))
        q_df = pd.DataFrame(columns=['q_clean'])
        q_df.loc[0, 'q_clean'] = tokens
        q_df['q_clean'] = word_lemmatizer(q_df.q_clean)
        q_df.replace(to_replace="\[.", value='', regex=True, inplace=True)
        q_df.replace(to_replace="'", value='', regex=True, inplace=True)
        q_df.replace(to_replace=" ", value='', regex=True, inplace=True)
        q_df.replace(to_replace='\]', value='', regex=True, inplace=True)

        d_cosines = []
        query_vector = self.__gen_vector_T(q_df['q_clean'])
        # matrix representation of the sparse matrix
        for d in self.tfidf_tran.A:
            d_cosines.append(self.__cosine_sim(query_vector, d))

        out = np.array(d_cosines).argsort()[-self.k:][::-1]
        d_cosines.sort()
        df_result = pd.DataFrame()
        for i, index in enumerate(out):
            df_result.loc[i, 'index'] = str(index)
            df_result.loc[i, 'subject'] = self.data['subject'][index]
        for j, simScore in enumerate(d_cosines[-self.k:][::-1]):
            df_result.loc[j, 'score'] = simScore
        return df_result
