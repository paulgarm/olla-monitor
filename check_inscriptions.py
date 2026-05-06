import requests
from bs4 import BeautifulSoup
import sys

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
    "https://olladenuria.cat/olla-classica/#inscripcions",
]

TARGET = "inscripcions.cat/olladenuria2026"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}

def check_url(url):
    fetch_url = url.split("#")[0]
    try:
        response = requests.get(fetch_url, timeout=15, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"ERREUR {url}: {e} -> ignore")
        return False

    html = response.text.lower()
    if TARGET in html:
        print(f"INSCRIPTIONS 2026 OUVERTES sur {url} !")
        return True

    print(f"OK - {url} ({response.status_code})")
    return False

def check():
    detected = False
    for url in URLS:
        if check_url(url):
            detected = True
    if detected:
        sys.exit(1)
    else:
        print("Surveillance continue...")
        sys.exit(0)

if __name__ == "__main__":
    check()
