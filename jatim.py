import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from requests.auth import HTTPBasicAuth

import config
from lib import push

dataModel = {
    "komoditas": "LELE",
    "daerah": "REGION",
    "harga": 0,
    "source": "http://fishinfojatim.net/dashboard/dashharga",
    "source-slug": "FSH-JTM",
    "method": "SCRAPING",
    "data-type": "DATACOLLECTOR",
    "tanggal": "",
}

today = "2021-01-01"

if len(sys.argv) > 1:
    today = sys.argv[1]
    endDate = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()

today_convert = datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)

while True:
    today_convert = today_convert - timedelta(days=1)
    today_format = today_convert.strftime("%d/%m/%Y")
    if today_convert.strftime("%Y-%m-%d") == endDate.strftime("%Y-%m-%d"):
        break
    URL = dataModel['source']
    query = {
        'tgl1' : {today_format},
        'tgl2' : {today_format},
        'ikan' : 'all',
        'pasar' : 'null',
        'jenis' : '0',
        'kota' : 'all'
    }
    getData = requests.get(URL, params=query)

    if getData.status_code != 200:
        print("ERROR")
        sys.exit(1)

    parser = BeautifulSoup(getData.text, 'html.parser')
    scrapData = parser.find_all("tr")[1:-1]
    bar = Bar(f'Crawl Data From {today_format}', max=len(scrapData))
    for dataTable in scrapData:
        items = dataTable.find_all("td")
        harga = items[3].get_text().split(",")[0].replace("Rp. ","").replace(".","").replace(" ","")
        dataModel['komoditas'] = items[1].get_text()
        dataModel['daerah'] = items[2].get_text()
        dataModel['harga'] = int(harga)
        dataModel['tanggal'] = today_convert.strftime("%Y-%m-%d")
        saveToAPI = push(dataModel)
        if saveToAPI != 200:
            print("error to save")
        bar.next()
    bar.finish()