import requests
from bs4 import BeautifulSoup
import smtplib
import os
import sys
from email.mime.text import MIMEText

URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
]

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

def check_page(url):
    try:
        response = requests.get(url, timeout=15, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"ERREUR {url}: {e} -> ignore")
        return False, ""

    soup = BeautifulSoup(response.text, "html.parser")
    html = response.text.lower()
    reasons = []

    # Signal 1 : lien vers le formulaire 2026 sur inscripcions.cat
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        if "inscripcions.cat" in href and "2026" in href:
            reasons.append(f"Lien inscripcions 2026 trouve: {a['href']}")

    # Signal 2 : le bouton INSCRIPCIONS OBERTES a un vrai lien (non vide)
    for a in soup.find_all("a"):
        if a.get_text(strip=True).upper() == "INSCRIPCIONS OBERTES":
            href = a.get("href", "").strip()
            if href and href not in ("#", "", "javascript:void(0)"):
                reasons.append(f"Bouton INSCRIPCIONS OBERTES actif: {href}")

    if reasons:
        detail = "\n".join(reasons)
        print(f"DETECTION sur {url}:\n{detail}")
        return True, detail

    print(f"OK - {url} ({response.status_code})")
    return False, ""

def check():
    all_reasons = []
    for url in URLS:
        detected, reason = check_page(url)
        if detected:
            all_reasons.append(f"{url}:\n{reason}")

    if all_reasons:
        body = "Les inscriptions 2026 semblent ouvertes !\n\n"
        body += "\n\n".join(all_reasons)
        body += "\n\nhttps://olladenuria.cat/olla-classica/#inscripcions"
        send_email("ALERTE - Inscriptions Olla de Nuria 2026 ouvertes !", body)
        sys.exit(1)
    else:
        send_email(
            "Olla de Nuria - Verification OK",
            "Pas d inscriptions 2026 detectees. Surveillance continue."
        )
        sys.exit(0)

if __name__ == "__main__":
    check()
