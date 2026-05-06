import requests
from bs4 import BeautifulSoup
import sys

URL = "https://olladenuria.cat/olla-classica/"

def check():
    response = requests.get(URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    text = soup.get_text().lower()
    html = response.text.lower()

    if "olladenuria2026" in html:
        print("INSCRIPTIONS 2026 DETECTEES !")
        sys.exit(1)

    if "inscripcions obertes" in text and "2026" in text:
        print("INSCRIPTIONS 2026 OUVERTES !")
        sys.exit(1)

    print("Pas encore ouvert. Surveillance continue...")
    sys.exit(0)

if __name__ == "__main__":
    check()
