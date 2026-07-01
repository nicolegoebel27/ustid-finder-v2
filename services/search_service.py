from providers.website_provider import WebsiteProvider
from services.vat_service import VATService


class SearchService:

    def __init__(self):
        self.website_provider = WebsiteProvider()
        self.vat_service = VATService()

    def search_company(
        self,
        company,
        street,
        number,
        zip_code,
        city,
        country
    ):

        website = self.website_provider.find_website(
            company,
            street,
            number,
            zip_code,
            city,
            country
        )

        result = {
            "website": "",
            "vat": "",
            "source": "",
            "status": ""
        }

        if website is None:
            result["status"] = "Keine Website gefunden"
            return result

        vat_result = self.vat_service.find_vat(website)

        result["website"] = website
        result["vat"] = vat_result["vat"]
        result["source"] = "Website"
        result["status"] = vat_result["status"]

        return result
