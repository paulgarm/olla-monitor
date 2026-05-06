import requests
from bs4 import BeautifulSoup
import sys

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
]

def check_url(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()
    html = response.text.lower()

    if "olladenuria2026" in html:
        print(f"INSCRIPTIONS 2026 DETECTEES sur {url} !")
        return True

    if "inscripcions obertes" in text and "2026" in text:
        print(f"INSCRIPTIONS 2026 OUVERTES sur {url} !")
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
