import sys
from datetime import datetime

import kkp
import jakarta
import jatim

dataModel = {
    "komoditas": "",
    "daerah": "",
    "harga": 0,
    "source": "URL",
    "source-slug": "",
    "method": "API/SCRAPING",
    "data-type": "DATACOLLECTOR/MARKETPLACE/ARTICLE",
    "tanggal": datetime.now().date().strftime("%Y-%m-%d"),
}

URLs = {
    "WPI-KKP": "http://wpi.kkp.go.id/info_harga_ikan/server.php",
    "IP-JKT": "https://infopangan.jakarta.go.id/api/price/series_by_commodity",
    "FSH-JTM": "http://fishinfojatim.net/dashboard/dashharga"
}

if __name__ == '__main__':
    print("Available Web to Crawl:")
    for index, (key, value) in enumerate(URLs.items()):
        print(f"{index+1} {key} {value}")
    target = input("Pick target: ")
    if len(sys.argv) > 1:
        dataModel["tanggal"] = sys.argv[1]
        endDate = datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
    else:
        dataModel["tanggal"] = input("Tanggal awal crawl (yyyy-mm-dd)")
        dataModel["tanggal"] = datetime.strptime(dataModel["tanggal"], "%Y-%m-%d").date()
        endDate = input("Tanggal akhir crawl (yyyy-mm-dd)")
        endDate = datetime.strptime(endDate, "%Y-%m-%d").date()

    

    

