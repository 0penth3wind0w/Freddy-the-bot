import os
import shutil

import requests
from bs4 import BeautifulSoup

from datetime import date
TODAY = date.today()
BASE_ROUTE = os.environ.get('BASE_ROUTE')
os.path.curdir

def get_wp_url() -> str:
    header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36"}
    url = "https://www.bing.com"
    response = requests.get(url, headers=header)

    soup = BeautifulSoup(response.text, "html.parser")
    wp_path = soup.find(id="preloadBg").get("href")
    idx = wp_path.index('&')
    wp_url = url + wp_path[:idx].replace("1920x1080", "UHD")
    return wp_url

def download_wallpaper() -> str:
    wp_url = get_wp_url()
    
    wp_name = "../image/wallpaper/{0}.jpg".format(TODAY)
    print(os.path.curdir)
    with requests.get(wp_url, stream=True) as r:
        with open(wp_name, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return "{0}.jpg".format(TODAY)

def wallpaper_exist() -> bool:
    wallpapar = "../image/wallpaper/{0}.jpg".format(TODAY)
    if os.path.isfile(wallpapar):
        return True
    return False

def local_wallpaper() -> str:
    return "{0}/image/wallpaper/{1}.jpg".format(BASE_ROUTE, TODAY)

if __name__ == "__main__":
    download_wallpaper()