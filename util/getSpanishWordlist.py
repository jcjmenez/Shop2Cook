import requests
from bs4 import BeautifulSoup

url = "https://www.linguasorb.com/spanish/food-word-list"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')
tables = soup.find_all('table')

#  Looking for the table with the classes 'wikitable' and 'sortable'
words = []
table = soup.find('table')
for row in table.find_all('tr'):
    columns = row.find_all('td')
    if columns[1].text != " " and columns[1].text != "\n" and columns[1].text != "":
        print(columns[1].text)
        words.append(columns[1].text.split(" ")[0])

with open("palabras-comida.txt", "w") as f:
    for w in words:
        f.write(w + "\n")