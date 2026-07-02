import time
import requests

from app.config import SERPAPI_KEY


class WebsiteProvider:

    BASE_URL = "https://serpapi.com/search.json"

    def __init__(self):
        self.blacklist = [
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

    def find_website(
        self,
        company,
        street,
        number,
        zip_code,
        city,
        country
    ):

        if not SERPAPI_KEY:
            print("SERPAPI_KEY fehlt.")
            return None

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

        # maximal 3 Versuche
        for attempt in range(3):

            try:

                response = requests.get(
                    self.BASE_URL,
                    params=params,
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                # kleine Pause gegen Rate-Limits
                time.sleep(1.0)

                # Knowledge Graph bevorzugen
                kg = data.get("knowledge_graph")

                if kg:
                    website = kg.get("website")

                    if website:
                        return website

                # Organische Treffer durchsuchen
                results = data.get("organic_results", [])

                for result in results:

                    link = result.get("link", "")

                    if not link:
                        continue

                    link_lower = link.lower()

                    if any(domain in link_lower for domain in self.blacklist):
                        continue

                    return link

                return None

            except requests.exceptions.Timeout:

                print(f"Timeout bei {company} (Versuch {attempt + 1}/3)")

                time.sleep(2)

            except requests.exceptions.RequestException as e:

                print(f"Fehler bei {company}: {e}")

                time.sleep(2)

        print(f"Website für '{company}' konnte nicht gefunden werden.")

        return None
