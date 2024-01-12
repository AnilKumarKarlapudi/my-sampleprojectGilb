from selenium.webdriver.remote.webelement import WebElement


class DisplayElement:

    def __init__(self, name: str, amount: float):
        self.name = name
        self.amount = amount

    def __str__(self):
        return f"{self.name} - ${self.amount}"

    @classmethod
    def from_element(cls, element: WebElement):
        """
        Create a DisplayElement from a WebElement
        Args:
            element (WebElement): WebElement to create the DisplayElement from
        Return:
            DisplayElement
        """
        item_text = element.text
        parts = item_text.split('\n')
        name = parts[0]
        amount = float(parts[1].replace('$', ''))

        return cls(name, amount)


class DisplayItem(DisplayElement):

    def __init__(self, name: str, amount: float):
        super().__init__(name, amount)


class DisplayDiscount(DisplayElement):

    def __init__(self, name: str, amount: float):
        super().__init__(name, amount)
