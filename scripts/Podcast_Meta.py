
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import pandas as pd
import json
import re

table_name = 'PodcastFinal_REAL_Alphabet_attempt'

class SavePodcast_meta(object):
    
    def __init__(self, table_name, Letter):
        #initiate the Mongo Server
        client = MongoClient()
        db = client['Podcast']
        # Access/Initiate Table
        self.Podcasts = db[table_name]
        self.letter   = Letter

    def _get_podcast_genres(self):
        Itunes_base_url = 'https://itunes.apple.com/ug/genre/podcasts/id26?mt=2'
        html = requests.get(Itunes_base_url)
        soup = BeautifulSoup(html.text)
        self.df_genre = pd.DataFrame(columns=['Genre', 'Link'])
        for i,genre in enumerate(soup.findAll(attrs={'class' : 'top-level-genre'})):
            temp = [str(genre.findAll(text=True)[0]), genre['href']]
            self.df_genre.loc[i] = temp
    
    def get_data(self):
        self._get_podcast_genres()
        failed=[]
        n=0
        for link in self.df_genre.Link:
            letter_link = link + '&letter=' + self.letter
            stuff = BeautifulSoup(requests.get(letter_link).content)
            pages_seen=[]
            try:
                for pages in stuff.find('ul',attrs={'class' :'list paginate'}):
                    try:
                        b = pages.find('a').get('href')
                        if b in pages_seen:
                            continue
                        else:
                            pages_seen.append(b)
                    except:
                        continue
            except:
                pages_seen.append(letter_link)

            for p_url in pages_seen:
                soup2        = BeautifulSoup(requests.get(p_url).content)
                podcast_list = soup2.find(attrs={'class':'grid3-column'})
                for podcast in podcast_list.findAll('a'):
                    n += 1
                    if n % 100 == 0:
                        print "*",
                    podcast_name = podcast.findAll(text=True)[0]
                    podcast_link = podcast['href']

                    ##get Json
                    podcast_id   = re.search('\/id(\d+)',podcast['href']).group(1)
                    json_link    = 'https://itunes.apple.com/lookup?id=' + podcast_id
                    try:
                        j            = requests.get(json_link)
                        j            = j.json()
                        jsonfile     = j['results'][0]
                        rss          = str(jsonfile['feedUrl'])
                        #get link
                        soup3        = BeautifulSoup(requests.get(rss).content)
                        summaries = []
                        for rss_summary  in soup3.findAll('itunes:summary'):
                            new = rss_summary.getText()
                            summaries.extend(new)
                        text = ' '.join(summaries)

                        #place into mongoDB
                        self.Podcasts.insert_one( {'PodcastName':podcast_name, 
                                              'PodcastLink': podcast_link, 
                                              'PodcastRSS' :text,
                                              'PodcastJson': jsonfile})
                    except:
                        print (podcast_name + ": Failed")
                        failed.append(podcast_id)
            del pages_seen[:]