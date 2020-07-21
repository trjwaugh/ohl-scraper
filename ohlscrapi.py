import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import pandas as pd

#in url: players/{digit} i assume is season since inception, goes up by 1 every year. for reference 2019-20 is 68.
# ctrl + F other variables and replace digit with the season you wish to scrape.

season = "68"

url = 'https://ontariohockeyleague.com/stats/players/{season}'.format(season = season)
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')

seasons_url = "http://lscluster.hockeytech.com/feed/?feed=modulekit&view=seasons&key=%s&fmt=json&client_code=ohl&lang=en&league_code=&fmt=json"
teamsbyseason_url = "http://lscluster.hockeytech.com/feed/?feed=modulekit&view=teamsbyseason&key=%s&fmt=json&client_code=ohl&lang=en&season_id=68&league_code=&fmt=json"
statviewtype_url = "http://lscluster.hockeytech.com/feed/?feed=modulekit&view=statviewtype&type=topscorers&key=%s&fmt=json&client_code=ohl&lang=en&league_code=&season_id=68&first=0&limit=200&sort=active&stat=all&order_direction="

key = soup.find('div', id='stats')['data-feed_key']

r = requests.get(seasons_url % key)
seasons_data = json.loads(r.text)

r = requests.get(teamsbyseason_url % key)
teamsbyseason_data = json.loads(r.text)

r = requests.get(statviewtype_url % key)
statviewtype_data = json.loads(r.text)
d = json.loads(r.text)

# Individual Player
df = pd.DataFrame(d)
h = df.loc['Statviewtype', 'SiteKit'][0].keys()
headers = list(h)
stats_list = df.loc['Statviewtype', 'SiteKit']

stats = []
for value in stats_list:
    stats.append(value)

#All players stats from season
s = pd.DataFrame(stats)
s.to_csv(r'C:\Users\timwa\Desktop\OHL-stats.csv', index=False)

