import sys
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import requests
from progress.bar import Bar

from lib import push

URL = "https://infopangan.jakarta.go.id/api/price/series_by_commodity"

query = {
    'public' : 1,
    'cid': 30, # 28 (Ikan Bandeng Sedang), 29 (Ikan Mas), 30 (Ikan Lele)
    'm': 5, # month
    'y': 2021 # year
}

COMMODITIES = {
    28: "Ikan Bandeng (Sedang)",
    29: "Ikan Mas",
    30: "Ikan Lele"
}

dataModel = {
    "komoditas": "LELE",
    "daerah": "REGION",
    "harga": 0,
    "source": "https://infopangan.jakarta.go.id/publik/report_commodity",
    "source-slug": "IP-JKT",
    "method": "API",
    "data-type": "DATACOLLECTOR",
    "tanggal": datetime.now().date().strftime("%Y-%m-%d"),
}

endDate = datetime.now().date() - timedelta(days=31)

if len(sys.argv) > 1:
    dataModel["tanggal"] = sys.argv[1]
    endDate = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()

today = datetime.strptime(dataModel["tanggal"], "%Y-%m-%d").date()

print(f"Start collecting from {today.strftime('%B %Y')} to {endDate.strftime('%B %Y')}")

today = today + relativedelta(months=1)

while True:
    today = today + relativedelta(months=-1)
    if today.strftime("%m %Y") == endDate.strftime("%m %Y"):
        print("This is the end of the crawling")
        break
    query['m'] = today.strftime("%-m")
    query['y'] = today.strftime("%Y")
    for cid in range(28, 31):
        print(f"{COMMODITIES[cid]} {today.strftime('%B %Y')}")
        query['cid'] = cid
        getData = requests.get(URL, params=query)

        if getData.status_code != 200:
            sys.exit(1)

        data = getData.json()['data']

        for market in data:
            
            dataModel['daerah'] = market['name']
            bar = Bar(f'Processing to get {dataModel["daerah"]}', max=len(market['series']))
            for day, price in market['series'].items():
                dataModel['komoditas'] = COMMODITIES[cid]
                dataModel['harga'] = int(price)
                dataModel['tanggal'] = f"{query['y']}-{query['m']}-{day}"
                saveToAPI = push(dataModel)
                if saveToAPI != 200:
                    print("Can't Save The Data")
                    break
                bar.next()
            bar.finish()
