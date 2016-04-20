# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 10:39:34 2016

@author: Crystal.Humphries
"""

from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("../data/Podcast_additional_info.csv", low_memory=False)
Titles = df.Title.values[0:200]

# home page
@app.route('/')
def index():
    #text = [str(request.form['user_input'])]
    #page = 'The predicted section name is: '
    return render_template('index.html', title='Hello!', seq=Titles)

@app.route('/recommender', methods=['GET','POST'])
def recommender():
    select = request.form.get('Podcast')
    return(str(select))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


#def word_counter():
#    text = [str(request.form['user_input'])]
#    page = 'The predicted section name is: '
#    return page + predict_section_name(text)
