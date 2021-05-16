# coding: utf8
from bs4 import BeautifulSoup
from bs4.builder import HTML
import csv
import requests

# steals metadata for all paintings, including the url for the thumbnail
# which is what ill use for the color analysis, because i only need a broad
# color profile (4-5 colors?)
# each museum has it's own csv file under it's name

with open('webscraping/artwork/museums.html', 'r', encoding='utf-8') as src:
    museumsoup = BeautifulSoup(src, 'lxml')

def parse_pages(museum_url, filewriter):
    url = museum_url + '?ut%5Bpage%5D=' + str(0)
    src = requests.get(url).text
    soup = BeautifulSoup(src, 'lxml')
    ul0 = soup.find('ul', class_='uu-column uu-column-first uu-column-0')
    ul1 = soup.find('ul', class_='uu-column uu-column-last uu-column-1')
    i = 1
    while(ul1.li is not None):
            parse_ul(ul0, filewriter)
            parse_ul(ul1, filewriter)
            i += 1
            url = museum_url + '?ut%5Bpage%5D=' + str(i)
            src = requests.get(url).text
            soup = BeautifulSoup(src, 'lxml')
            ul0 = soup.find('ul', class_='uu-column uu-column-first uu-column-0')
            ul1 = soup.find('ul', class_='uu-column uu-column-last uu-column-1')
            print(i)
    if(ul0.li is not None):
        parse_ul(ul0, filewriter)       

def parse_ul(ul, filewriter):
    for li in ul.find_all("li"):
        thumbnail = li.img['src']
        #todo: streamline this process
        title = li.find('a', 'uu-exhibit-title-link')
        year = li.find('div', 'uu-exhibit-title')
        artist = li.find('a', 'uu-author-link')
        country = li.find('a', 'uu-country-link')
        if title is not None:
            title = title.text.encode('utf-8')
        if year is not None:
            year = year.text.split()[-1].encode('utf-8')
        if artist is not None:
            artist = artist.text.encode('utf-8')
        if country is not None:
            country = country.text.encode('utf-8')
        filewriter.writerow([title, artist, year, country, thumbnail])

uls = museumsoup.find_all('ul', 'uu-creators-list uu-el--reset')
for ul in uls:
    i = 0
    for li in ul.find_all('li', 'uu-creator uu-el--reset clearfix'):
        if(i<1):
            museum = li.a
            museumurl = 'https://useum.org' + museum['href']
            print(museumurl)
            museumname = li.find('span', 'uu-name').text
            path = 'data/Art/'
            filename = path + ''.join(c for c in museumname if c.isalnum()) + '.csv'
            with open(filename, 'w') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow(['Title', 'Artist', 'Year', 'Country', 'Thumbnail'])
                parse_pages(museumurl, filewriter)
        i +=1

print('done my guy')
        



