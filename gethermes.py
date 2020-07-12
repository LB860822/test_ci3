#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import requests
import time

parser = argparse.ArgumentParser()
parser.description='please enter parameters ...'
parser.add_argument('-s', '--search', help='what you want to search', dest='search', type=str, default='lindy')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='hermes.txt')
args = parser.parse_args()

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

session = requests.session()
session.get('https://ecp.hermes.com/is-logged-in?country=pl&locale=pl_en', headers=headers)
#html_set_cookie = requests.utils.dict_from_cookiejar(session.cookies)
#print(html_set_cookie)

time.sleep(2)

resulttotal = 0
resultproduct = {}

for search in args.search.split(','):
    print(search)
    productList = session.get('https://bck.hermes.com/product?locale=pl_en&searchterm='+search+'&sort=relevance', headers=headers).content.decode('utf-8')
    print(productList)
    productlistjson = json.loads(productList)
    total = productlistjson['total']
    if total > 0:
        resulttotal += total
        resultproduct[search]=total
    time.sleep(5)

if resulttotal > 0:
    print(resultproduct)
    with open(args.out, 'w') as filehermes:
        for product in resultproduct.keys():
            filehermes.write('Please note that %d %s products are on sale : https://www.hermes.com/pl/en/search/?s=%s#||Category\n'%(resultproduct[product], product, product))
else:
     raise Exception('no products found')

