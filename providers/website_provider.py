import requests

from app.config import SERPAPI_KEY


class WebsiteProvider:

    BASE_URL = "https://serpapi.com/search.json"

    def find_website(
        self,
        company,
        street,
        number,
        zip_code,
        city,
        country
    ):

        # Prüfen, ob der API-Key vorhanden ist
        if not SERPAPI_KEY:
            raise Exception(
                "SERPAPI_KEY wurde nicht gefunden. Bitte die .env-Datei prüfen."
            )

        # Suchanfrage aufbauen
        query = f"{company} {zip_code} {city} Impressum"

        params = {
            "engine": "google",
            "q": query,
            "google_domain": "google.de",
            "gl": "de",
            "hl": "de",
            "num": 10,
            "api_key": SERPAPI_KEY
        }

        blacklist = [
            "facebook.com",
            "linkedin.com",
            "instagram.com",
            "youtube.com",
            "gelbeseiten.de",
            "dasoertliche.de",
            "northdata.de",
            "firmenwissen.de",
            "creditreform.de",
            "webwiki.de",
            "11880.com",
            "cylex.de"
        ]

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("organic_results", [])

            if not results:
                return None

            for result in results:

                link = result.get("link", "")

                if not link:
                    continue

                link_lower = link.lower()

                if any(domain in link_lower for domain in blacklist):
                    continue

                return link

            return None

        except requests.exceptions.RequestException as e:
            raise Exception(f"SerpAPI-Verbindungsfehler: {e}")

        except Exception as e:
            raise Exception(f"Fehler bei der Websuche: {e}")
