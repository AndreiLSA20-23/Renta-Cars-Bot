import requests
from bs4 import BeautifulSoup
import lxml
from dbWorker import Database
from config import DB_FILE

db = Database(DB_FILE)

def Parser():
    url = 'https://rentacars.kz/'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')
    container = soup.select_one('div.car-list')
    products = container.find_all('div',{'itemtype':'http://schema.org/Product'})

    carslist = []
    for product in products:
        name = product.find('span',{'itemprop':'name'}).text
        if 'Range Rover' in name:
            model = 'Range Rover'
        elif 'Kia' in name:
            model = 'Kia'
        elif 'Toyota' in name:
            model = 'Toyota'
        elif 'Lexus' in name:
            model = 'Lexus'
        elif 'Hyndai' in name or 'Hyundai' in name:
            model = 'Hyundai'
        elif 'Mercedes' in name:
            model = 'Mercedes'
        elif 'Chevrolet' in name:
            model = 'Chevrolet'
        elif 'Mitsubishi' in name:
            model = 'Mitsubishi'
        amount = product.find('div',{'class':'amount'}).text
        fuel = product.find('div',{'class':'fuel'}).text
        trans = product.find('div',{'class':'trans'}).text
        pricesblock = product.find_all('div',{'class':'price-line'})
        prices = []
        for priceblock in pricesblock:
            prices.append(priceblock.text.replace('\n', ' '))
        pricelist = ''.join([price for price in prices])
        deposit = product.find('div',{'class':'deposit'}).text
        charblock = product.find('div',{'class':'char-block'}).text.replace('\n', ' ')
        stock = 1
        img_name = product.find('img',{'itemprop':'image'})['src']
        if '/CARS/' in img_name:
            new_img = img_name.replace('/CARS', '')
            img = requests.get(url + img_name).content
            with open(f'images{new_img}', 'wb') as f:
                f.write(img)
            if (name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images{new_img}') not in carslist:
                carslist.append((name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images{new_img}', model))
        elif '/1/' in img_name:
            new_img = img_name.replace('/1/', '')
            img = requests.get(url + img_name).content
            with open(f'images/{new_img}', 'wb') as f:
                f.write(img)
            if (name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images/{new_img}') not in carslist:
                carslist.append((name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images/{new_img}', model))
        else:
            img = requests.get(url + img_name).content
            with open(f'images{img_name}', 'wb') as f:
                f.write(img)
            if (name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images{img_name}') not in carslist:
                carslist.append((name, amount, fuel, trans, pricelist, deposit, charblock, stock, f'images{img_name}', model))

    sql_insert_to_table_almati = "INSERT INTO almati (name, amount, fuel, trans, pricelist, deposit, charblock, stock, image, model) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
    db.insert_cars(sql_insert_to_table_almati, carslist)

Parser()