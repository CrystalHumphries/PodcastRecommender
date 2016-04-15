
twitter_handle = []
podcast_name   = []

for pod in Podcasts.find({}, {'PodcastName':1, '_id':0}):
    pName = pod['PodcastName']
    podcast_name.append(pName)
    if re.search('|', pName):
        pName = pName.split('|')[0].strip()
    try:
        twitter_search = 'https://twitter.com/search?q=%22' + pName + '%22%20%23podcast&src=typd&lang=en'
        attempt = requests.get(twitter_search)
        soup = BeautifulSoup(attempt.content)
        b = soup.find('div', {'class':'ProfileCard ProfileCard--wide js-actionable-user'})
        handle = b.find('button').get("title")
        twitter_handle.append(handle)
    except:
        try:
            twitter_search = 'https://twitter.com/search?q=%22' + pName + '&src=typd'
            attempt = requests.get(twitter_search)
            soup = BeautifulSoup(attempt.content)
            b = soup.find('div', {'class':'ProfileCard ProfileCard--wide js-actionable-user'})
            handle = b.find('button').get("title")
            twitter_handle.append(handle)
        except:
            handle="None"
            twitter_handle.append(handle)