import requests
import pandas as pd

def get_price(ids):
    ids_str = ";".join(ids)
    template = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=26&nm="
    url = template + ids_str

    print(url)

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.wildberries.ru',
        'Referer': 'https://www.wildberries.ru/catalog/180225973/detail.aspx',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.931 YaBrowser/23.9.3.931 Yowser/2.5 Safari/537.36',
        'sec-ch-ua': '^\^"Chromium^\^";v=^\^"116^\^", ^\^"Not)A;Brand^\^";v=^\^"24^\^", ^\^"YaBrowser^\^";v=^\^"23^\^"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '^\^"Windows^\^"',
    }

    response = requests.get(url = url, headers = headers)

    return response.json()


def filter_data(response):
    products = []

    data = response.get('data', {}).get('products', None)

    if data != None and len(data) > 0:
        for product in data:
            products.append({
                'id': product.get('id', None),
                'brand' : product.get('brand', None), 
                'name' : product.get('name', None),
                'sale': product.get('sale', None),
                'priceU' : float(product.get('priceU', None)) / 100 if product.get('priceU', None) != None else None,
                'salePriceU' : float(product.get('salePriceU', None)) / 100 if product.get('salePriceU', None) != None else None
                })
            
    return(products)


def price_check(products, prices):
    best_price = []
    for num, product in enumerate(products):
        print("Wb", product['salePriceU'])
        print("Target", prices[num])
        if product['salePriceU'] <= prices[num]:
            best_price.append(product['id'])
    return best_price

def process(item_id, target_prices):

    str_ids = [str(id) for id in item_id]

    response = get_price(str_ids)
    products = filter_data(response)

    best_prices_ids = price_check(products, target_prices)

    return best_prices_ids