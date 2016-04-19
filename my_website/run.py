# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:39:34 2016

@author: Crystal.Humphries
"""

from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("../data/Podcast_additional_info.csv", low_memory=False)
Titles = df.Title.values[0:200]

# home page
@app.route('/')
def index():
    return render_template('index.html', title='Hello!', seq=Titles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

