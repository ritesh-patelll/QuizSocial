from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

def TopListCreator():
    # Initialising Variables.
    start = 1
    today = datetime.today().strftime('%Y-%m-%d')
    # year = re.findall('\d{4}', today)[0]
    year = '2022'

    categories = ['feature,tv_movie', 'tv_series']
    titles = {}

    # Getting the Lists.
    for type in categories:
        items = []
        url = f'https://www.imdb.com/search/title/?title_type={type}&release_date={year}-01-01,{today}&view=simple&sort=num_votes,desc&start={start}&count=250&ref_=adv_nxt'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html5lib").body
        
        for div in soup.find_all("div", {"class": "lister list detail sub-list"}):
            for span in div.find_all("span", {"class": "lister-item-header"}):
                for link in span.find_all('a', href=True):
                    imdb_id = re.sub('\n|/title/|/', '', str(link.get('href'))).strip()
                    
                    if len(items) != 100:
                        if imdb_id != '' and imdb_id not in items:
                            items.append(imdb_id)
                            
        titles[type] = items[0:100]
        
    film_links = titles['feature,tv_movie']
    series_links = titles['tv_series']

    with open('top_imdb_movie.txt', 'w') as f:
        for line in film_links:
            f.write(line)
            f.write('\n')

    with open('top_imdb_series.txt', 'w') as f:
        for line in series_links:
            f.write(line)
            f.write('\n')