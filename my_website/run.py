# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:39:34 2016

@author: Crystal.Humphries
"""

from flask import Flask, render_template, request
import pandas as pd
import unicodedata
import graphlab as gl
import numpy as np

app = Flask(__name__)

df = pd.read_pickle("../data/FinalPodcastMeta.pkl")
df.reset_index(inplace=True)
df.Title = df.Title.apply(lambda x: unicode(x.decode('utf-8')))
df.Title= df['Title'].str.lower()
df.iTunesSubtitle = df.iTunesSubtitle.apply(lambda x: unicode(x.decode('utf-8')))
d = gl.load_model("../src/item_model")


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
        ls_info.append(temp2[keep].loc[i].to_dict())
    return ls_info

# home page
@app.route('/')
def index():
    return render_template('index.html', title='New Podcasts', seq=df.Title.str.title().values)

@app.route('/recommender', methods=['GET','POST'])
def recommender():
    select = request.form.get('Podcast')
    pod = unicode(select.decode('utf-8'))
    temp = df[df.Title==pod.lower()]
    pred = d.get_similar_items(gl.SArray([pod.title()]))
    pred = pd.Series(pred['similar'])
    pred = pred.str.lower()
    temp2 = df[df.Title.isin(pred)]
    prediction_info = get_meta(temp2)

    return render_template('Recommendations.html', title='Hello!', 
                           podcast=pod, summary=temp.iTunesSummary.values[0],
                           ratings = temp.RatingCount.values[0],
                            AvgStars=temp.AverageRating.values[0],
                            predictions = prediction_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
