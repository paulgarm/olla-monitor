import requests
from bs4 import BeautifulSoup
import smtplib
import os
import sys
from email.mime.text import MIMEText
from datetime import date, datetime, timezone

# URL directe du formulaire - signal le plus fiable
DIRECT_URL = "https://inscripcions.cat/preinscolla2026/formulari_inscripcio"

# URLs de la page Olla de Nuria a surveiller en complement
URLS = [
    "https://olladenuria.cat/",
    "https://olladenuria.cat/olla-classica/",
]

# Patterns a chercher dans les pages olladenuria.cat
TARGETS = [
    "preinscolla2026",
    "inscripcions.cat/olladenuria2026",
    "inscripcions.cat/olla2026",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0 Safari/537.36"
}

EMAIL_USER = os.environ.get("EMAIL_USER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
EMAIL_TO = "soulard.paul@gmail.com"

INTENSIVE_START = date(2026, 5, 11)
DAILY_HOUR_UTC = 7

def should_run():
    today = date.today()
    if today >= INTENSIVE_START:
        return True, "mode intensif (toutes les 5min)"
    now_utc = datetime.now(timezone.utc)
    if now_utc.hour == DAILY_HOUR_UTC:
        return True, f"mode journalier (avant le {INTENSIVE_START})"
    return False, f"mode journalier - pas encore l heure"

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

def check_direct_url():
    """Verifie directement le formulaire d inscription - signal prioritaire."""
    try:
        r = requests.get(DIRECT_URL, timeout=15, headers=HEADERS)
        print(f"Direct URL status: {r.status_code} - {DIRECT_URL}")
        if r.status_code == 200:
            return True, f"Page formulaire accessible (200): {DIRECT_URL}"
        return False, ""
    except Exception as e:
        print(f"ERREUR direct URL: {e} -> ignore")
        return False, ""

def check_page(url):
    """Verifie les pages olladenuria.cat en complement."""
    try:
        response = requests.get(url, timeout=15, headers=HEADERS)
        response.raise_for_status()
    except Exception as e:
        print(f"ERREUR {url}: {e} -> ignore")
        return False, ""
    soup = BeautifulSoup(response.text, "html.parser")
    html = response.text.lower()
    reasons = []
    for target in TARGETS:
        if target in html:
            reasons.append(f"Pattern trouve: '{target}'")
    for a in soup.find_all("a"):
        if a.get_text(strip=True).upper() == "INSCRIPCIONS OBERTES":
            href = a.get("href", "").strip()
            if href and href not in ("#", "", "javascript:void(0)"):
                reasons.append(f"Bouton INSCRIPCIONS OBERTES actif: {href}")
    if reasons:
        return True, "\n".join(reasons)
    print(f"OK - {url} ({response.status_code})")
    return False, ""

def check():
    run, mode = should_run()
    if not run:
        print(f"Skip: {mode}")
        sys.exit(0)

    print(f"Verification en cours - {mode}")
    all_reasons = []

    # Signal 1 (prioritaire) : URL directe du formulaire
    detected, reason = check_direct_url()
    if detected:
        all_reasons.append(reason)

    # Signal 2 : pages olladenuria.cat
    for url in URLS:
        detected, reason = check_page(url)
        if detected:
            all_reasons.append(f"{url}: {reason}")

    if all_reasons:
        body = "Les inscriptions 2026 sont ouvertes !\n\n"
        body += "\n\n".join(all_reasons)
        body += f"\n\nLien direct: {DIRECT_URL}"
        send_email("ALERTE - Inscriptions Olla de Nuria 2026 ouvertes !", body)
        sys.exit(1)
    else:
        send_email(
            "Olla de Nuria - Verification OK",
            f"Mode: {mode}\nFormulaire non accessible (404).\nPas d inscriptions detectees."
        )
        sys.exit(0)

if __name__ == "__main__":
    check()
