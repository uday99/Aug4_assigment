import  requests
from bs4 import BeautifulSoup
import sqlite3 as sql
conn=sql.connect("scrapdata.db")
curs=conn.cursor()
#curs.execute("create table myscrap( s_name text ,s_price real ,s_rating text)")
#conn.close()
#print("Table created")

Url="https://www.amazon.in/s?k=Laptops"


def get_scrap(Url):
    res = requests.get(url=Url).content
    soup = BeautifulSoup(res, 'html.parser')
    names = []
    prices = []
    ratings = []
    for name in soup.find_all('a', href=True, attrs={'class': 'a-link-normal a-text-normal'}):
        my = name.find('span', attrs={'class': 'a-size-medium a-color-base a-text-normal'})
        names.append(my.text)

    for price in soup.find_all('a', href=True, attrs={'class': 'a-size-base a-link-normal a-text-normal'}):
        pr = price.find('span', attrs={'class': 'a-price-whole'})
        prices.append(pr.text)

    for rating in soup.find_all('i', attrs={'class': 'a-icon a-icon-star-small a-star-small-4 aok-align-bottom'}):
        rt = rating.find('span', attrs={'class': 'a-icon-alt'})
        print(rt.text)
        ratings.append(rt.text)

    for n, p, r in zip(names, prices, ratings):
        name = n
        price = p
        rating = r
        print(n)
        print(p)
        print(r)
        curs.execute('''insert into myscrap values(?,?,?)''', (name, price, rating))

    # print(names)
    # print(prices)
    # print(ratings)




get_scrap(Url)

conn.commit()
print('complete')
curs.execute('''select * from myscrap''')
results=curs.fetchall()
print(results)
conn.close()


