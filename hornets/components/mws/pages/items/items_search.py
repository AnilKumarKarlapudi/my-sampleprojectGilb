from abc import ABC, abstractmethod


class ItemSearchStrategy(ABC):

    @abstractmethod
    def search(self):
        pass


class ItemSearchByPLU(ItemSearchStrategy):

    def __init__(self, department_to_search=None, item_type_to_search=None):
        self.department_to_search = department_to_search
        self.item_type_to_search = item_type_to_search

    def search(self, item_page, search_input_value: str):
        item_page._add_search_options(self.department_to_search, self.item_type_to_search)
        return item_page._search_by_plu(search_input_value=search_input_value)


class ItemSearchByDescription(ItemSearchStrategy):

    def __init__(self, department_to_search=None, item_type_to_search=None):
        self.department_to_search = department_to_search
        self.item_type_to_search = item_type_to_search

    def search(self, item_page, search_input_value: str):
        item_page._add_search_options(self.department_to_search, self.item_type_to_search)
        return item_page._search_by_description(search_input_value=search_input_value)


class ItemSearchByScanCode(ItemSearchStrategy):

    def __init__(self, department_to_search=None, item_type_to_search=None):
        self.department_to_search = department_to_search
        self.item_type_to_search = item_type_to_search

    def search(self, item_page, search_input_value: str):
        item_page._add_search_options(self.department_to_search, self.item_type_to_search)
        return item_page._search_by_scan_code(search_input_value=search_input_value)


class ItemSearchByReceiptDescription(ItemSearchStrategy):

    def __init__(self, department_to_search=None, item_type_to_search=None):
        self.department_to_search = department_to_search
        self.item_type_to_search = item_type_to_search

    def search(self, item_page, search_input_value: str):
        item_page._add_search_options(self.department_to_search, self.item_type_to_search)
        return item_page._search_by_receipt_description(search_input_value=search_input_value)
