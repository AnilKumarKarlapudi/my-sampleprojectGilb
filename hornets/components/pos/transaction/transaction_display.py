from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.payment_method import PaymentMethod
from hornets.components.pos.pos_locators import TransactionDisplayLocators
from hornets.components.pos.pos_section import PosSection
from hornets.components.pos.transaction.total_transaction import TotalTransaction
from hornets.components.pos.transaction.watermark import Watermark
from hornets.models.manual_discount.models import ManualDiscount
from hornets.models.display_element import DisplayItem, DisplayDiscount
from hornets.utilities.log_config import logger


class TransactionDisplay(PosSection):
    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.transaction = []
        self.total_transaction = TotalTransaction()
        self.watermark = Watermark(self.driver)

    def to_dict(self, payment_method: PaymentMethod = None) -> dict:
        """
        Return the transaction display as a dict
        Args:
            payment_method (PaymentMethod): Payment method used for the transaction
        Return:
            dict: Transaction display as a dict
        """
        return {
            "transaction": [(item.name, item.amount) for item in self.transaction],
            "total_transaction": {
                "total": self.total_transaction.total,
                "basket_count": self.total_transaction.basket_count,
            },
            "payment_method": payment_method,
            "watermark": self.watermark.status
        }

    def add_item(self, item: DisplayItem):
        """
        Add an item to the transaction display
        Args:
            item (DisplayItem): Item to add
        """
        logger.info(f"Adding item {item.name} to transaction display")
        item = self.find_elements(TransactionDisplayLocators.ITEMS)[-1]
        display_item = DisplayItem.from_element(item)
        self.transaction.append(display_item)
        self.total_transaction.add_item(display_item)

    def add_discount(self, discount: ManualDiscount):
        """
        Add a discount to the transaction display
        Args:
            discount (Discount): Discount to add
        """
        logger.info(f"Adding discount {discount.name} to transaction display")
        discount = self.find_element(TransactionDisplayLocators.DISCOUNT)
        display_discount = DisplayDiscount.from_element(discount)
        self.transaction.append(display_discount)
        self.total_transaction.add_discount(display_discount)

    def get_last_item_added(self) -> DisplayItem:
        """
        Get the last item added to the transaction display
        Return:
            DisplayItem: Last item added to the transaction display
        """
        return self.transaction[-1]

    def wait_for_transaction_to_be_completed(self):
        """
        Wait for the transaction to be completed
        Return:
            bool: True if the transaction is completed, False otherwise
        """
        return self.watermark.wait_for_transaction_to_be_completed()

    def get_values_from_transaction_display(self) -> dict:
        """
        Get the values from the transaction display
        Return:
            dict: Values from the transaction display
        """
        return {
            "total": float(self.find_element(TransactionDisplayLocators.TOTAL_AMOUNT).text.replace("$", "")),
            "basket_count": int(self.find_element(TransactionDisplayLocators.BASKET_COUNT).text)
        }
