from bs4 import BeautifulSoup
from bs4.builder import HTML
import csv
import re
import requests

# todo: make loop for each museum

# rips source code from website as txt object on the base website
# the images are all one one page hidden after ::after, and dont
# load all together in the dom this is back end 'last page' youll
# have to iterate thru these 0-47 inclusive for natgal
with open('museums.html', 'r', encoding='utf-8') as src:
    museumsoup = BeautifulSoup(src, 'lxml')

def parse_pages(museum_url, filewriter):
    # todo: change loop to fit all museums
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
            title = title.text
        if year is not None:
            year = year.text.split()[-1]
        if artist is not None:
            artist = artist.text
        if country is not None:
            country = country.text
        filewriter.writerow([title, artist, year, country, thumbnail])

'''with open('nationalgallerywash.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['Title', 'Artist', 'Year', 'Country', 'Thumbnail'])
    museum_url = 'https://useum.org/collection/National-Gallery-of-Art-Washington'
    parse_pages(museum_url, filewriter)'''

uls = museumsoup.find_all('ul', 'uu-creators-list uu-el--reset')
for ul in uls:
    for li in ul.find_all('li', 'uu-creator uu-el--reset clearfix'):
        museum = li.a
        museumurl = 'https://useum.org' + museum['href']
        museumname = li.find('span', 'uu-name').text

        filename = ''.join(c for c in museumname if c.isalnum()) + '.csv'
        with open(filename, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(['Title', 'Artist', 'Year', 'Country', 'Thumbnail'])
            museum_url = 'https://useum.org/collection/National-Gallery-of-Art-Washington'
            parse_pages(museum_url, filewriter)

print('done my guy')
        



