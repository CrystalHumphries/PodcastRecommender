# PodcastRecommender

ThePodcastRecommender app is live at www.ThePodcastRecommender.com

A novel recommender for Podcasts.



### Project Description
A recommender system to find similar podcasts. Currently, users have to sift through data on iTunes to attempt to find similar podcasts. Here I leverage podcast similarity along with 'user' data to create a podcast recommender. This recommender will take one or more podcasts and use that information to recommend similar podcasts. Using this system will enable the user to find a similar podcast in a much easier manner.

### Data Collection
Podcast Data was collected with the following tools:
 - BeautifulSoup
 - Itunes Website: Podcast Metadata
 - Bing: Podcast Twitter Handles
 - Twitter: Twitter API
 - MongoDB: Used for Data Storage


  Scripts:
    - Podcast_Meta.py: scraping website and placing data into mongodb
    - ParrallelMEta.py: running Podcast_Meta.py in parallel
    - ObtainHandles.py: using data from itunes to grab twitter handles
    - GetTwitterFollowers.py: Obtaining Twitter followers

### Data Cleaning and FeatureEngineering
I used SVD, K-means, and several NLP methods including TF-IDF and NMF to generate features for the podcast recommender. 

  clean_podcast_csv.py: obtains the saved data frame and cleans it for prediction. 
  PodcastFeatureEngineering.py: is a child of clean_podcast_csv.py and allows for calling additional functions for feature engineering. 
  
### Model Creation
  I used scikit-learn and plotly to perform and visualize the exploratory data analysis. 
  
### Website
  Using Flask, I created ThePodcastRecommender.com.
  run.py is the flask app I created to generate the website

![alt text][logo]

[logo]:https://github.com/CrystalHumphries/PodcastRecommender/blob/master/my_website/static/img/PodcastRecommendersite.jpg "Website Screen Shot"

