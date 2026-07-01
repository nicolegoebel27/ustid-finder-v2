from providers.base_provider import BaseProvider


class WebsiteProvider(BaseProvider):

    def __init__(self):
        pass

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

        print("Suche:", query)

        # HIER kommt später die eigentliche Suche hinein.

        return None
