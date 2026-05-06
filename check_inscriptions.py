import requests
from bs4 import BeautifulSoup
import sys

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
    "https://olladenuria.cat/olla-classica/#inscripcions",
]

# Chaine exacte qui n'existe que quand les inscriptions 2026 sont ouvertes
TARGET = "inscripcions.cat/olladenuria2026"

def check_url(url):
    fetch_url = url.split("#")[0]
    response = requests.get(fetch_url, timeout=10)
    response.raise_for_status()
    html = response.text.lower()

    # Debug : afficher tous les liens inscripcions.cat trouves
    soup = BeautifulSoup(response.text, "html.parser")
    for a in soup.find_all("a", href=True):
        if "inscripcions.cat" in a["href"].lower():
            print(f"  Lien inscripcions.cat trouve: {a['href']}")

    if TARGET in html:
        print(f"INSCRIPTIONS 2026 OUVERTES sur {url} !")
        return True

    print(f"OK - {url}")
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
