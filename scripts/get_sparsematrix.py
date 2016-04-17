
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
CV = CountVectorizer()
from scipy.sparse import csr_matrix
from PodcastFeatureEngineering import Podcast_Features
import graphlab as gl

client = MongoClient()
# Access/Initiate Database
db = client['Podcast']
# Access/Initiate Table
Podcast_twitter = db['PodcastTwitter_handles']
print Podcast_twitter.count()

practice = []
n=0
for pod in Podcast_twitter.find({}, {'Title':1, '_id':0, 'TwitterFollowers':1}):
    try:
        if 'TwitterFollowers' in pod and pod['TwitterFollowers'] and pod['TwitterFollowers'][0]!='None':
            practice.append(pod)
            n+=1
    except:
        pass
print n


def create_sparse_matrix(list_of_followers):
    list_of_strings = []
    list_of_titles = []
    for ls in list_of_followers:
        x = ' '.join([ str(x) for x in ls['TwitterFollowers']])
        list_of_strings.append(x)
        list_of_titles.append(ls['Title'])
    return list_of_strings, list_of_titles


strings,titles = create_sparse_matrix(practice)
final = CV.fit_transform(strings)

a = csr_matrix.sum(final, axis=0)
a = np.array(a).reshape(a.shape[1],)
sparse = final.toarray()
mask = a>1
sparse_mat = sparse[:,mask]
item_matrix=gl.SFrame(sparse_mat)

item_matrix.save("IHavebeensaved.gl")