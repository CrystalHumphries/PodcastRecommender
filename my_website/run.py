# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:39:34 2016

@author: Crystal.Humphries
"""

from flask import Flask, render_template, request
import pandas as pd
import unicodedata

app = Flask(__name__)


def whatisthis(s):
    try:
        s.decode('ascii')
        return s
    except:
        return s.decode("utf-8")



df = pd.read_pickle("../data/FinalPodcastMeta.pkl")
df = df.iloc[0:200, :]
df.Title = df.Title.apply(lambda x: unicode(x.decode('utf-8')))
df.Title= df['Title'].str.lower()
df.iTunesSubtitle = df.iTunesSubtitle.apply(lambda x: unicode(x.decode('utf-8')))



def stars(x):
    ls = ['stars'] * x
    if x < 5:
        no_stars = ['noStars']* (5-x)
        ls.extend(no_stars)
    return ls
    
def get_meta(temp2):
    ls_info = []
    temp2['Title'] = temp2['Title'].str.title()
    keep = ['AverageRating','Link','iTunesSubtitle', 'Title']
    for i in temp2.index:
        ls_info.append(temp2[keep].iloc[i].to_dict())
    return ls_info


# home page
@app.route('/')
def index():
    return render_template('index.html', title='Hello!', seq=df.Title.values)


@app.route('/recommender', methods=['GET','POST'])
def recommender():
    select = request.form.get('Podcast')
    pod = unicode(select)
    temp = df[df.Title==pod.lower()]
    pred = df.Title[0:10].values
    temp2 = df[df.Title.isin(pred)]
    prediction_info = get_meta(temp2)
    return render_template('Recommendations.html', title='Hello!', 
                           podcast=pod, summary=temp.iTunesSummary.values[0],
                           ratings = temp.RatingCount.values[0],
                            AvgStars=temp.AverageRating.values[0],
                            predictions = prediction_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
