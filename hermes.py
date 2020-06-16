#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from selenium import webdriver
import time

headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}

parser = argparse.ArgumentParser()
parser.description='please enter parameters ...'
parser.add_argument('-s', '--search', help='what you want to search', dest='search', type=str, default='lindy')
parser.add_argument('-o', '--output', help='output file', dest='out', type=str, default='hermes.txt')
args = parser.parse_args()

url='https://www.hermes.com/pl/en/search/?s='+args.search+'#||Category'

# Get the Firefox profile object
profile = webdriver.firefox.webdriver.FirefoxProfile()
# Disable images
profile.set_preference('permissions.default.image', 2)
# Disable Flash
profile.set_preference(
    'dom.ipc.plugins.enabled.libflashplayer.so', 'false'
)
#profile.native_events_enabled = True
options = webdriver.firefox.options.Options()
options.headless = True
firefox = webdriver.Firefox(firefox_profile=profile, options=options, timeout=60)
firefox.get(url)

geted = False
errors='unknown errors'
content=''

try:
    time.sleep(5)
    subtitles = firefox.find_elements_by_xpath('//div[@class="sub-title"]')
    if len(subtitles) == 0:
        geted = True
    else:
        errors=subtitles[0].text
        print(errors)
    maintitle = firefox.find_element_by_xpath('//div[@class="main-title"]')
    content=maintitle.text
    print(content)
    with open(args.out, 'w') as filehermes:
        filehermes.write(content+'\n'+url)
except Exception:
    geted = False
    print('exception')

firefox.close()
firefox.quit()

if not geted:
    raise Exception(errors)
