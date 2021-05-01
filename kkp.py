from datetime import datetime, timedelta
import time
import sys

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

dataModel = {
    "komoditas": "",
    "daerah": "",
    "harga": 0,
    "source": "http://wpi.kkp.go.id/info_harga_ikan/",
    "source-slug": "WPI-KKP",
    "method": "API",
    "data-type": "DATACOLLECTOR",
    "tanggal": datetime.now().date(),
}

if len(sys.argv) > 1:
    dataModel["tanggal"] = datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
    endDate = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()

WPI_COMMODITIES = [
    "BANDENG", "CAKALANG", "GURAMI", 
    "KEMBUNG", "LAYANG", "LELE", "NILA",
    "PATIN", "TONGKOL", "UDANG PUTIH"
]

today = dataModel["tanggal"] + timedelta(days=1)

while True:
    today = today - timedelta(days=1)
    if today.strftime("%Y-%m-%d") == endDate.strftime("%Y-%m-%d"):
        break
    print(f"Crawl {today}")
    query["_"] = int(time.mktime(today.timetuple()))
    getData = requests.get(URL, params=query)
    if getData.status_code != 200:
        break
    for dataDaerah in getData.json()["data"]:
        daerah = dataDaerah[0]
        bar = Bar(f'Processing to {daerah}', max=len(dataDaerah[1:-1]))
        for index, hargaKomoditas in enumerate(dataDaerah[1:-1]):
            dataModel['komoditas'] = WPI_COMMODITIES[index-1]
            dataModel['daerah'] = daerah
            dataModel['harga'] = int(hargaKomoditas.replace(",", "")) if hargaKomoditas != "-" else 0
            dataModel['tanggal'] = today.strftime("%Y-%m-%d")
            saveToAPI = push(dataModel)
            if saveToAPI != 200:
                print("error to save")
            bar.next()
        bar.finish()
                

