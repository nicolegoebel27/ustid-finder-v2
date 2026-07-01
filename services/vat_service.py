import re
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.config import REQUEST_TIMEOUT, USER_AGENT


class VATService:

    def __init__(self):
        self.headers = {
            "User-Agent": USER_AGENT
        }

    def find_vat(self, website):

        if not website:
            return {
                "vat": "",
                "status": "Keine Website"
            }

        try:

            response = requests.get(
                website,
                headers=self.headers,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()

            html = response.text

            # Direkt auf der Startseite suchen
            vat = self.extract_vat(html)

            if vat:
                return {
                    "vat": vat,
                    "status": "USt-ID gefunden"
                }

            # Impressum suchen
            soup = BeautifulSoup(html, "lxml")

            impressum_url = self.find_impressum(soup, website)

            if impressum_url:

                response = requests.get(
                    impressum_url,
                    headers=self.headers,
                    timeout=REQUEST_TIMEOUT
                )

                response.raise_for_status()

                vat = self.extract_vat(response.text)

                if vat:
                    return {
                        "vat": vat,
                        "status": "USt-ID im Impressum gefunden"
                    }

            return {
                "vat": "",
                "status": "Keine USt-ID gefunden"
            }

        except Exception as e:

            return {
                "vat": "",
                "status": f"Fehler: {e}"
            }

    def extract_vat(self, text):

        patterns = [

            # Deutschland
            r"\bDE\s?[0-9]{9}\b",

            # Schreibweise USt-IdNr.: DE123456789
            r"USt[- ]?IdNr\.?\s*:?\s*(DE\s?[0-9]{9})",

            # VAT ID
            r"VAT\s*ID\s*:?\s*(DE\s?[0-9]{9})",

            # Umsatzsteuer-Identifikationsnummer
            r"Umsatzsteuer[- ]?Identifikationsnummer\s*:?\s*(DE\s?[0-9]{9})",

        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE
            )

            if match:

                if match.lastindex:
                    return match.group(1).replace(" ", "")

                return match.group().replace(" ", "")

        return ""

    def find_impressum(self, soup, base_url):

        suchbegriffe = [

            "impressum",
            "imprint",
            "legal",
            "legal notice",
            "kontakt",
            "contact"

        ]

        for link in soup.find_all("a", href=True):

            text = link.get_text(" ", strip=True).lower()

            href = link["href"]

            if any(wort in text for wort in suchbegriffe):

                return urljoin(base_url, href)

        return None
