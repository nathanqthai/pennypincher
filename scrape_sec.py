#!/usr/bin/env python3 

from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse
import requests
import threading
import queue

def url2soup(url):
    page = requests.get(url)
    page = page.text.replace("&nbsp", "")
    return BeautifulSoup(page, "lxml")

def process_year(year_url, year_data): 
    year_soup = url2soup(year_url)
    table = year_soup.find('p', id='archive-links').find_next('table')
    for tr in table.find_all('tr'):
        row = tr.find_all('td')
        if len(row) < 3 or not(row[0].a):
            continue
        try:
            year_data.put(
                    [base_url+row[0].a['href'], 
                     parse(row[1].text).strftime('%Y%m%d'), 
                     row[2].text.replace('\n', ' ').replace('\r', '').rstrip()])
        except:
            print("ERROR:")
            print([base_url+row[0].a['href'], row[1].text, row[2].text])
            continue

base_url = "https://www.sec.gov"
top_page = "/litigation/admin.shtml"

top_soup = url2soup(base_url+top_page)
archive_links = top_soup.select('p[id="archive-links"] > a[href]')
archive_urls = [base_url+tag['href'] for tag in archive_links]

threads = []
data = queue.Queue()
for url in archive_urls:
    t = threading.Thread(target=process_year, args=(url, data))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

with open('sec_litigations.csv', 'w') as fd:
    while(not(data.empty())):
        fd.write(','.join(data.get())+'\n')
