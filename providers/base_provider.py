from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def find_website(
        self,
        company,
        street,
        number,
        zip_code,
        city,
        country
    ):
        pass
