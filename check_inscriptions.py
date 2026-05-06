import requests
from bs4 import BeautifulSoup
import smtplib
import os
import sys
from email.mime.text import MIMEText

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
    "https://olladenuria.cat/olla-classica/#inscripcions",
]

TARGET = "inscripcions.cat/olladenuria2026"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}

EMAIL_USER = os.environ.get("EMAIL_USER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_TO = "soulard.paul@gmail.com"

def send_email(subject, body):
    if not EMAIL_USER or not EMAIL_PASSWORD:
        print("Pas de credentials email, skip envoi")
        return
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = EMAIL_TO
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        print(f"Email envoye: {subject}")
    except Exception as e:
        print(f"Erreur envoi email: {e}")

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
    detected = any(check_url(url) for url in URLS)
    if detected:
        send_email(
            "ALERTE - Inscriptions Olla de Nuria 2026 ouvertes !",
            "Les inscriptions 2026 sont ouvertes !\nhttps://olladenuria.cat/olla-classica/#inscripcions"
        )
        sys.exit(1)
    else:
        send_email(
            "Olla de Nuria - Verification OK",
            "Pas d inscriptions 2026 detectees. Surveillance continue."
        )
        sys.exit(0)

if __name__ == "__main__":
    check()
