from datetime import datetime, timedelta
import time

import requests
from progress.bar import Bar
from requests.auth import HTTPBasicAuth

from lib import push

URL = "http://wpi.kkp.go.id/info_harga_ikan/server.php"

query = {
    "draw": 3,
    "start": 0,
    "length": 100,
    "_": datetime.strptime("2021-02-04", "%Y-%m-%d").date()
}

data = []

WPI_COMMODITIES = [
    "BANDENG", "CAKALANG", "GURAMI", 
    "KEMBUNG", "LAYANG", "LELE", "NILA",
    "PATIN", "TONGKOL", "UDANG PUTIH"
]

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
            saveToAPI = push({
                "komoditas": WPI_COMMODITIES[index-1],
                "daerah": daerah,
                "harga": int(hargaKomoditas.replace(",", "")) if hargaKomoditas != "-" else 0,
                "source": source,
                "source-slug": source_slug,
                "method": method,
                "data-type": data_type,
                "tanggal": today.strftime("%Y-%m-%d")
            })
            if saveToAPI.status_code != 200:
                print("error to save")
            bar.next()
        bar.finish()
                

