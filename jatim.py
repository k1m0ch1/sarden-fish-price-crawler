import sys
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from requests.auth import HTTPBasicAuth

import config

dataModel = {
    "komoditas": "LELE",
    "daerah": "REGION",
    "harga": 0,
    "source": "URL",
    "source-slug": "",
    "method": "API/SCRAPING",
    "data-type": "DATACOLLECTOR/MARKETPLACE/ARTICLE",
    "tanggal": "",
}

today = "2021-01-01"
today_convert = datetime.strptime(today, "%Y-%m-%d").date() + timedelta(days=1)
source = "http://fishinfojatim.net/dashboard/dashharga"
source_slug = "FSH-JTM"
method = "SCRAPING"
data_type = "DATACOLLECTOR"

while True:
    today_convert = today_convert - timedelta(days=1)
    today_format = today_convert.strftime("%d/%m/%Y")
    if today_convert.strftime("%Y-%m-%d") == "2020-01-01":
        break
    URL = f"http://fishinfojatim.net/dashboard/dashharga"
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
        push = requests.post(
            f"{config.API_URL}{config.ENDPOINT_SAVE_LOG}",
            auth=HTTPBasicAuth(config.AUTH_USERNAME, config.AUTH_PASSWORD),
            json={
                "komoditas": items[1].get_text(),
                "daerah": items[2].get_text(),
                "harga": int(harga),
                "source": source,
                "source-slug": source_slug,
                "method": method,
                "data-type": data_type,
                "tanggal": today_convert.strftime("%Y-%m-%d")
            }
        )
        if push.status_code != 200:
            print("error to save")
        bar.next()
    bar.finish()