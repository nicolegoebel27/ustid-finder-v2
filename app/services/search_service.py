from providers.website_provider import WebsiteProvider


class SearchService:

    def __init__(self):
        self.website_provider = WebsiteProvider()

    def search_company(
        self,
        company,
        street,
        number,
        zip_code,
        city,
        country
    ):

        query = f"{company} {street} {number} {zip_code} {city} {country}"

        website = self.website_provider.find_website(query)

        result = {
            "website": "",
            "vat": "",
            "source": "",
            "status": ""
        }

        if website is None:
            result["status"] = "Keine Website gefunden"
            return result

        result["website"] = website
        result["source"] = "Website"

        # Die USt-ID-Suche bauen wir im nächsten Schritt ein.
        result["status"] = "Website gefunden"

        return result
