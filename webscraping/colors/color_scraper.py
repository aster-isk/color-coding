from bs4 import BeautifulSoup
import requests
import csv

# hehehehe my pantone now :3

pantoneurl = requests.get('https://www.easycalculation.com/colorconverter/pantone-to-hex-table.php').text
soup = BeautifulSoup(pantoneurl, 'lxml')
table = soup.find('div', 'table clearfix').table

with open('pantone_hex.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',', 
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for row in table.find_all('tr'):
            text = row.text.split()
            print(" ".join(text[:-1]) + ' ' + text[-1])
            filewriter.writerow([" ".join(text[:-1]), text[-1]])
    


