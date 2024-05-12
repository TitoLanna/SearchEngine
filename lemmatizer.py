from collections import defaultdict
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import pandas as pd


def word_lemmatizer(data):
    stopwords_arr = stopwords.words('english')
    # create a default-dict object and set the default value to Noun
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    df_lemmatized = pd.DataFrame()
    for idx, entry in enumerate(data):
        finalized_words = []
        lemmatizer = WordNetLemmatizer()
        # get the POS (Part of Speech) tag for a word whether it is Noun(N) or Verb(V) or others
        for word, tag in pos_tag(entry):
            # check for alphabets and stopwords
            if len(word) > 1 and word not in stopwords_arr and word.isalpha():
                lemmatized_word = lemmatizer.lemmatize(word, tag_map[tag[0]])
                finalized_words.append(lemmatized_word)
                # word cleaning
                df_lemmatized.loc[idx, 'final_keywords'] = str(finalized_words)
                df_lemmatized.replace(to_replace="\[.", value='', regex=True, inplace=True)
                df_lemmatized.replace(to_replace="'", value='', regex=True, inplace=True)
                df_lemmatized.replace(to_replace=" ", value='', regex=True, inplace=True)
                df_lemmatized.replace(to_replace='\]', value='', regex=True, inplace=True)

    return df_lemmatized
