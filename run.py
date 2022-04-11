import requests
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

url = "https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv"
headers = {"Accept-Language": "en-US, en;q=0.5"}
results = requests.get(url, headers=headers)

soup = BeautifulSoup(results.text, "html.parser")

#initiate data storage
titles = []
years = []
links = []
time = []
imdb_ratings = []
metascores = []
votes = []
us_gross = []

movie_div = soup.find_all('div', class_='lister-item mode-advanced')

#our loop through each container
for container in movie_div:

        #name
        name = container.h3.a.text
        titles.append(name)
        
        link= container.h3.a['href']
        links.append(link)
        
        year = container.h3.find('span', class_='lister-item-year text-muted unbold').text
        years.append(year)
        
        runtime = container.p.find('span', class_='runtime').text if container.p.find('span', class_='runtime').text else '-'
        time.append(runtime)
        
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)
        
        m_score = container.find('span', class_='metascore').text if container.find('span', class_='metascore') else '-'
        metascores.append(m_score)
        
         #there are two NV containers, grab both of them as they hold both the votes and the grosses
        nv = container.find_all('span', attrs={'name': 'nv'})
        
        #filter nv for votes
        vote = nv[0].text
        print(vote)
        votes.append(vote)
        
        #filter nv for gross
        grosses = nv[1].text if len(nv) > 1 else '-'
        us_gross.append(grosses)
        

        
print(titles)
print(links)
print(years)
print(time)
print(imdb)
print(imdb_ratings)
print(metascores)
print(votes)
print(us_gross)
        
#pandas dataframe        
movies = pd.DataFrame({
'movie': titles,
'links' : links,
'year': years,
'timeMin': time,
'imdb': imdb_ratings,
'metascore': metascores,
'votes': votes,
'us_grossMillions': us_gross,
})

#cleaning data 
movies['year'] = movies['year'].str.extract('(\d+)').astype(int)
movies['timeMin'] = movies['timeMin'].str.extract('(\d+)').astype(int)
movies['metascore'] = movies['metascore'].astype(int)
movies['votes'] = movies['votes'].str.replace(',', '').astype(int)
movies['us_grossMillions'] = movies['us_grossMillions'].map(lambda x: x.lstrip('$').rstrip('M'))
movies['us_grossMillions'] = pd.to_numeric(movies['us_grossMillions'], errors='coerce')

#add dataframe to csv file named 'movies.csv'
movies.to_csv('movies.csv')
