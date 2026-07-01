import re
import requests
from bs4 import BeautifulSoup


class VATService:

    def __init__(self):
        pass

    def find_vat(self, website):

        if not website:
            return {
                "vat": "",
                "status": "Keine Website"
            }

        try:

            response = requests.get(
                website,
                timeout=15,
                headers={
                    "User-Agent": "Mozilla/5.0"
                }
            )

            if response.status_code != 200:
                return {
                    "vat": "",
                    "status": "Website nicht erreichbar"
                }

            html = response.text

            vat = self.extract_vat(html)

            if vat:

                return {
                    "vat": vat,
                    "status": "USt-ID gefunden"
                }

            soup = BeautifulSoup(html, "lxml")

            impressum = self.find_impressum(soup, website)

            if impressum:

                response = requests.get(
                    impressum,
                    timeout=15,
                    headers={
                        "User-Agent": "Mozilla/5.0"
                    }
                )

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
                "status": str(e)
            }

    def extract_vat(self, text):

        pattern = r"\bDE[0-9]{9}\b"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""

    def find_impressum(self, soup, base_url):

        for link in soup.find_all("a", href=True):

            text = link.get_text().lower()

            if "impressum" in text:

                href = link["href"]

                if href.startswith("http"):
                    return href

                return base_url.rstrip("/") + "/" + href.lstrip("/")

        return None
