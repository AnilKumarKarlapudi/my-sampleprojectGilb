from hornets.models.display_element import DisplayItem, DisplayDiscount


class TotalTransaction:

    def __init__(self, basket_count: int = 0, total: float = 0.0):
        self.basket_count = basket_count
        self.total = total
        self.reset_values()

    def add_item(self, item: DisplayItem):
        """
        Add an item to the transaction
        Args:
            item (DisplayItem): Item to add
        """
        self.basket_count += 1
        self.total += item.amount

    def add_discount(self, discount: DisplayDiscount):
        """
        Add a discount to the transaction
        """
        self.total += discount.amount

    def reset_values(self):
        """
        Reset the values of the transaction
        """
        self.basket_count = 0
        self.total = 0
