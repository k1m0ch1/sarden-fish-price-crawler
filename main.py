import config

from datetime import datetime, timedelta
import time

import requests
from progress.bar import Bar
from requests.auth import HTTPBasicAuth

URL = "http://wpi.kkp.go.id/info_harga_ikan/server.php"

query = {
    "draw": 3,
    "start": 0,
    "length": 100,
    #"_": datetime.now().date()
    "_": datetime.strptime("2021-02-04", "%Y-%m-%d").date()
}

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

data = []

WPI_COMMODITIES = [
    "BANDENG", "CAKALANG", "GURAMI", 
    "KEMBUNG", "LAYANG", "LELE", "NILA",
    "PATIN", "TONGKOL", "UDANG PUTIH"
]

print(config.API_URL)

today = query["_"] + timedelta(days=1)
while True:
    source = "http://wpi.kkp.go.id/info_harga_ikan/"
    source_slug = "WPI-KKP"
    method = "API"
    data_type = "DATACOLLECTOR"
    today = today - timedelta(days=1)
    if today.strftime("%Y-%m-%d") == "2017-12-31":
        break
    print(f"Crawl {today}")
    curr_timestamp = time.mktime(today.timetuple())
    getData = requests.get(URL, params=query)
    if getData.status_code != 200:
        break
    for dataDaerah in getData.json()["data"]:
        daerah = dataDaerah[0]
        bar = Bar(f'Processing to {daerah}', max=len(dataDaerah[1:-1]))
        for index, hargaKomoditas in enumerate(dataDaerah[1:-1]):
            push = requests.post(
                f"{config.API_URL}{config.ENDPOINT_SAVE_LOG}",
                auth=HTTPBasicAuth(config.AUTH_USERNAME, config.AUTH_PASSWORD),
                json={
                    "komoditas": WPI_COMMODITIES[index-1],
                    "daerah": daerah,
                    "harga": int(hargaKomoditas.replace(",", "")) if hargaKomoditas != "-" else 0,
                    "source": source,
                    "source-slug": source_slug,
                    "method": method,
                    "data-type": data_type,
                    "tanggal": today.strftime("%Y-%m-%d")
                }
            )
            if push.status_code != 200:
                print("error to save")
            bar.next()
        bar.finish()
                

