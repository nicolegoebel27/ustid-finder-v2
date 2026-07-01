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

        query = (
            f"{company} "
            f"{street} {number} "
            f"{zip_code} "
            f"{city} "
            f"{country}"
        )

        params = {
            "engine": "google",
            "q": query,
            "google_domain": "google.de",
            "gl": "de",
            "hl": "de",
            "api_key": SERPAPI_KEY
        }

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=20
            )

            response.raise_for_status()

            data = response.json()

            if "organic_results" not in data:
                return None

            for result in data["organic_results"]:

                link = result.get("link")

                if link:
                    return link

            return None

        except Exception as e:

            print("SerpAPI Fehler:", e)

            return None
