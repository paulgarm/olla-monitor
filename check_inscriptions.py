import requests
from bs4 import BeautifulSoup
import sys

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
    "https://olladenuria.cat/olla-classica/#inscripcions",
]

def check_url(url):
    fetch_url = url.split("#")[0]
    response = requests.get(fetch_url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Signal fiable : un lien <a> dont le href contient "inscripcions.cat" et "2026"
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if "inscripcions.cat" in href and "2026" in href:
            print(f"INSCRIPTIONS 2026 DETECTEES sur {url} ! Lien: {a['href']}")
            return True

    print(f"OK - Pas encore ouvert : {url}")
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
