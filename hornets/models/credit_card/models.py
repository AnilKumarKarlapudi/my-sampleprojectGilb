from hornets.components.constants import CARD_DATA
from hornets.models.credit_card.enums import CreditCardBrandEnum
from hornets.utilities.log_config import logger


class CreditCard:
    def __init__(self, card_brand: CreditCardBrandEnum, card_name: str, card_number: str):
        self.card_brand = card_brand.value
        self.card_name = card_name
        self.card_number = card_number
        self.card_data_raw = self._get_card_data()

    def __str__(self):
        return f"CreditCard(card_brand={self.card_brand}, card_name={self.card_name}, card_number={self.card_number})"

    def get_last_four_digits(self) -> str:
        logger.info(f"Getting last four digits of card number: {self.card_number}")
        return self.card_number[-4:]

    def process_payment(self, pos):
        raise NotImplementedError

    def _get_card_data(self):
        """
        Gets the card data from the card_data.json file.
        Returns:
            dict : Dictionary representing all the key/value pairs of the card
        """
        try:
            return CARD_DATA[self.card_brand][self.card_name]
        except KeyError:
            logger.error(f"Unable to find {self.card_name} within {self.card_brand} brand.")
            return {}


class MagstripeCreditCard(CreditCard):
    def __init__(self, card_brand: CreditCardBrandEnum, card_name: str, card_number: str):
        super().__init__(card_brand, card_name, card_number)

    def process_payment(self, pos):
        logger.info(f"Processing payment with magstripe credit card: {self}")
        pos._process_payment_with_magstripe_credit_card(self)


class EmvCreditCard(CreditCard):
    def __init__(self, card_brand: CreditCardBrandEnum, card_name: str, card_number: str):
        super().__init__(card_brand, card_name, card_number)

    def process_payment(self, pos):
        logger.info(f"Processing payment with EMV credit card: {self}")
        pos._process_payment_with_emv_credit_card(self)


class ContactlessCreditCard(CreditCard):
    def __init__(self, card_brand: CreditCardBrandEnum, card_name: str, card_number: str):
        super().__init__(card_brand, card_name, card_number)

    def process_payment(self, pos):
        logger.info(f"Processing payment with contactless credit card: {self}")
        pos._process_payment_with_contactless_credit_card(self)
