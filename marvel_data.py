from bs4 import BeautifulSoup
import requests
import json

def get_content_value(row_data):
    if row_data.find('li'):
        return [li.get_text(' ', strip=True).replace('\xa0','') for li in row_data.find_all('li')]
    else:
        return row_data.get_text(' ', strip=True).replace('\xa0','')

def get_info_box(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    info = soup.find('table', class_='infobox vevent')
    info_rows = info.find_all('tr')
    
    
    movie_info = {}
    for index, row in enumerate(info_rows):
        if index==0:
            movie_info['title'] = row.find('th').get_text()
        elif index==1:
            continue
        else:
            content_key = row.find('th').get_text(' ',strip=True)
            content_value = get_content_value(row.find('td'))
            movie_info[content_key] = content_value
    
    return movie_info
    
page = requests.get('https://en.wikipedia.org/wiki/List_of_Marvel_Cinematic_Universe_films')
soup = BeautifulSoup(page.content, 'html.parser')
movies = soup.select('.wikitable.plainrowheaders i')

base_path= 'https://www.wikipedia.org/'

movie_info_list = []

for index, movie in enumerate(movies):
    try:
        relative_path = movie.a['href']
        full_path = base_path + relative_path
        title = movie.a['title']
        
        movie_info_list.append(get_info_box(full_path))
    except:
        pass
     

def save_data(title,data):
    with open(title, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
        
def load_data(title):
    with open(title, encoding='utf-8') as f:
        return json.load(f)
  
save_data('marvel_data.json', movie_info_list)
