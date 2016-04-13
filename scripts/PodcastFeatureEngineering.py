
import pandas as pd
from clean_podcast_csv import PodcastCleaner
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.decomposition import NMF

class Podcast_Features(PodcastCleaner):
    
    def __init__(self, cleaned_df=None, text_vec_model=None):
        PodcastCleaner.__init__(self)
        if cleaned_df is None:
            self.df = self.get_clean_df()
        else:
            self.df = cleaned_df
        
        if text_vec_model is None:
            self.vec_model = self._text_model_create()
        else:
            self.vec_model = text_vec_model
        
        
    def get_NMF_topics(self):
        pass
    
    def print_top_words(model, feature_names, n_top_words):
        for topic_idx, topic in enumerate(model.components_):
            print("Topic #%d:" % topic_idx)
            print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()
    
    def _text_model_create(self):
        from sklearn.feature_extraction import text
        my_stop_words = text.ENGLISH_STOP_WORDS.union(['www', 'podcast', 'talkshoe', 'href'])
        self.vec_model = TfidfVectorizer(max_df=0.95, 
                                   ngram_range=(1, 3),
                                   min_df=3,
                                   stop_words=my_stop_words,
                                   )
    def call_nmf(self, text):
        nmf = NMF(n_components=20, random_state=1, alpha=.1, 
                  l1_ratio=.5).fit(self.vectorized_text)
        print("\nTopics in NMF model:")
        tfidf_feature_names = tfidf_vectorizer.get_feature_names()
        self.print_top_words(nmf, tfidf_feature_names, 20)
        
    def vectorize_text(self, col):
        if self.vec_model is None:
            self._text_model_create()
            print "hello"
        self.text = self.vec_model.fit_transform(df[col].values)