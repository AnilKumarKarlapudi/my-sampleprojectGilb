from typing import Optional, List

from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import DropdownOption
from hornets.components.exceptions import ElementNotFoundException, ElementNotSavedException
from hornets.components.mws.navigation_urls import ITEMS_PAGE_URL
from hornets.components.mws.pages.items.item import MwsItem
from hornets.components.mws.pages.items.items_search import ItemSearchByPLU
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.mws.mws_locators import ItemsMwsPageLocators, MainMwsPageLocators
from hornets.utilities.log_config import logger


class ItemsMwsPage(MwsPage):

    def __init__(self, driver: WebDriver, item_search_strategy=ItemSearchByPLU()):
        super().__init__(
            driver=driver,
            url=ITEMS_PAGE_URL,
            element_to_wait_for=ItemsMwsPageLocators.ADD,
        )
        self.item_search_strategy = item_search_strategy

    def save(self, item: MwsItem, message_to_check: str):
        """
        Clicks Save button and verifies if Item creation was successful.
        Args:
            item (Item): MwsItem
            message_to_check (str): Message to verify in success toast
        """
        if not self.is_save_enabled():
            raise ElementNotSavedException(f"Item {item.plu} could not be saved. Save button is disabled")

        self.click(locator_enum=ItemsMwsPageLocators.SAVE)

        if not self.information_has_been_saved(additional_message=message_to_check):
            raise ElementNotSavedException(f"Item {item.plu} save was not successful")

    def add_item(
            self,
            plu: str,
            description: str,
            department: DropdownOption,
            additional_options: Optional[dict] = None,
            price_option: Optional[int] = 1,
            unit_price: Optional[float] = None,
            deal_quantity: Optional[float] = None,
            deal_price: Optional[float] = None,
            save: Optional[bool] = True) -> MwsItem:
        """
        Adds an Item.
        Args:
            plu (str): PLU of the Item
            description (str): description of the Item
            department (DropdownOption): department of the Item
            additional_options (Optional[dict]): Item additional options to configure.
            price_option (Optional[int]): price option of the Item (options: 1, 2, 3, 4 or 5)
            unit_price (Optional[float]): unit price of the Item
            deal_quantity (Optional[float]): deal quantity of the Item
            deal_price (Optional[float]): deal price of the Item
            save (Optional[bool]): If True saves the item. If False Save button will not be pressed.
        Returns:
            _ (MwsItem):  Returns the created MwsItem
        Example:
            item_to_create = Item(
                PLU=f"0000040{random.randint(0, 100000)}",
                description="Test Item",
                department=ItemDepartmentEnum.DEPT_8,
                type=ItemTypeEnum.REGULAR_ITEM,
                price_option=1,
                unit_price=5.5
                )
            >>> items_page.add_item(item=item_to_create)
                MwsItem
            >>> items_page.add_item(item=item_to_create, save=False)
                None. Item is configured in Add Item screen but Save button is not pressed.

            options = {
                ItemsMwsPageLocators.DISCOUNTABLE: True,
                ItemsMwsPageLocators.RETURN_PRICE: base_item_to_create_in_mws.unit_price,
                ItemsMwsPageLocators.CASH_SWITCH: True,
                ItemsMwsPageLocators.CHECK_SWITCH: True,
                ItemsMwsPageLocators.MONEY_ORDER_SWITCH: True,
            }
            >>> items_page.add_item(item=item_to_create, options=options)
                MwsItem
        """
        item = MwsItem(
            driver=self.driver,
            plu=plu,
            description=description,
            department=department,
            price_option=price_option,
            unit_price=unit_price,
            deal_price=deal_price,
            deal_quantity=deal_quantity,
        )

        logger.info("Item to add: ")

        logger.info(item)
        self.click(locator_enum=ItemsMwsPageLocators.ADD)

        item.item_options.set_fields_value(fields_value={
            ItemsMwsPageLocators.PLU_INPUT: plu,
            ItemsMwsPageLocators.DESCRIPTION_INPUT: description,
            ItemsMwsPageLocators.DEPARTMENT_DROPDOWN: department
        })

        item.set_price_option(
            price_option=item.price_option,
            unit_price=item.unit_price,
            deal_price=item.deal_price,
            deal_quantity=item.deal_quantity
        )

        if additional_options:
            item.item_options.expand_all_page_sections()
            item.item_options.set_fields_value(fields_value=additional_options)

        if not save:
            logger.warning("Item was not created in MWS: save option disabled by user.")
            return None

        self.__save_button_enabler()
        self.save(item=item, message_to_check="Items")

        return item

    def search_items(self, search_input_value: Optional[str] = None) -> List[MwsItem]:
        """
        Search items using the criteria specified by current ItemSearchStrategy.
        Args:
            search_input_value (Optional[str]): Value to enter in search input.
        Returns:
            _ (List[MwsItem]): List of items that match search criteria.
        Examples:
            Search with no input and no filters to bring all items.
            >>> results = items_page.search_items()
            results -> [Item, Item, Item...]

            Search with no input and two filters to bring all regular items from Dept 1 .
            >>>items_page.item_search_strategy.department_to_search = ItemDepartmentEnum.DEPT_1
            >>>items_page.item_search_strategy.item_type_to_search = ItemTypeEnum.REGULAR_ITEM
            >>>results = items_page.search_items()
            results -> [Item, Item, Item...]

            Search item 001 by PLU (default strategy). No filters.
            >>> results = items_page.search_items(search_input_value="001")
            results bring all items that have 001 in their PLU.

            Search Generic Item by Description with department and type filters (changed default strategy)
            >>>items_page.item_search_strategy = ItemSearchByDescription(
            >>>                                     department_to_search=ItemDepartmentEnum.DEPT_1,
            >>>                                     item_type_to_search=ItemTypeEnum.REGULAR_ITEM)
            >>>results = items_page.search_items(search_input_value=item.description)
            results -> [GenericItem]
        """
        search_input = self.find_element(value_locator=ItemsMwsPageLocators.SEARCH_INPUT)
        search_input.clear()
        if not search_input_value:
            search_input_value = ""
        self.item_search_strategy.search(item_page=self, search_input_value=search_input_value)
        return self._get_search_results()

    def edit_item(self, item_plu: str, options_to_edit: dict, price_options_to_edit: Optional[dict] = None) -> MwsItem:
        """
        Edits an existing Item in MWS
        Args:
            item_plu (str): PLU of the Item to edit
            options_to_edit (dict): contains all the item options to edit
            price_options_to_edit: if present contains the new price option and prices for the Item
        Returns:
            item_to_edit (MwsItem): Updated Item with the new options passed
        Example:
            options_to_edit = {
            ItemsMwsPageLocators.DESCRIPTION_INPUT: "Edited Item",
            ItemsMwsPageLocators.DEPARTMENT_DROPDOWN: ItemDepartmentEnum.DEPT_2,
            ItemsMwsPageLocators.DISCOUNTABLE: True,
            ItemsMwsPageLocators.CHECK_SWITCH: True,
            ItemsMwsPageLocators.RETURN_PRICE: "5.5",
            }

            # Price options are handled separately due to some problematic behavior of the fields involved
            edited_price_options = {
                "price_option": 2,
                "unit_price": 9.99,
                "deal_quantity": 4
            }
            >>>edited_item = items_page.edit_item(
            >>>         item_plu=new_item_to_edit.plu,
            >>>         options_to_edit=options_to_edit,
            >>>         price_options_to_edit=edited_price_options)
            MwsItem
        """
        self.item_search_strategy = ItemSearchByPLU()
        found_items = self.search_items(search_input_value=item_plu)
        try:
            item_to_edit = next(found_item for found_item in found_items if found_item.plu == item_plu)
        except StopIteration:
            raise ElementNotFoundException(f"Item {item_plu} was not found")

        self.click(locator_enum=ItemsMwsPageLocators.EDIT, additional_attribute=item_plu)

        self.expand_all_page_sections()

        if price_options_to_edit:
            item_to_edit.set_price_option(
                price_option=price_options_to_edit.get("price_option"),
                unit_price=price_options_to_edit.get("unit_price", None),
                deal_price=price_options_to_edit.get("deal_price", None),
                deal_quantity=price_options_to_edit.get("deal_quantity", None)
            )

        item_to_edit.edit(options_to_edit=options_to_edit)

        self.__save_button_enabler()

        self.save(item=item_to_edit, message_to_check="Items")

        return item_to_edit

    def item_exists(self, item: MwsItem) -> bool:
        """
        Check if the specified item exists. Searchs by exact PLU.
        Args:
            item (Item): Item to search for.
        Returns:
            _ (bool): True if item was found in results. False if item was not found or search could not be made.
        """
        if not self.wait_for_page_to_load():
            logger.error("There was a problem returning to the main Items screen. Cannot verify if item was saved.")
            return False
        self.item_search_strategy = ItemSearchByPLU()
        results = self.search_items(search_input_value=item.plu)
        return any([item.plu == item_found.plu for item_found in results])

    def _search_by_plu(self, search_input_value: str):
        # Default search strategy. PLU/UPC radio button is selected by default in MWS.
        logger.info("Item Search Strategy: PLU")
        self.set_value(locator_enum=ItemsMwsPageLocators.SEARCH_INPUT, value=search_input_value)
        search_button = self.find_element(value_locator=ItemsMwsPageLocators.SEARCH_BUTTON)
        search_button.click()

    def _search_by_description(self, search_input_value: str):
        logger.info("Item Search Strategy: Description")
        self.click(locator_enum=ItemsMwsPageLocators.DESCRIPTION_RADIO_BUTTON)
        self.set_value(locator_enum=ItemsMwsPageLocators.SEARCH_INPUT, value=search_input_value)
        search_button = self.find_element(value_locator=ItemsMwsPageLocators.SEARCH_BUTTON)
        search_button.click()

    def _search_by_scan_code(self, search_input_value: str):
        logger.info("Item Search Strategy: Scan Code")
        self.click(locator_enum=ItemsMwsPageLocators.SCANCODE_RADIO_BUTTON)
        self.set_value(locator_enum=ItemsMwsPageLocators.SEARCH_INPUT, value=search_input_value)
        search_button = self.find_element(value_locator=ItemsMwsPageLocators.SEARCH_BUTTON)
        search_button.click()

    def _search_by_receipt_description(self, search_input_value: str):
        logger.info("Item Search Strategy: Receipt Description")
        self.click(locator_enum=ItemsMwsPageLocators.RECEIPTDESCRIPTION_RADIO_BUTTON)
        self.set_value(locator_enum=ItemsMwsPageLocators.SEARCH_INPUT, value=search_input_value)
        search_button = self.find_element(value_locator=ItemsMwsPageLocators.SEARCH_BUTTON)
        search_button.click()

    def _add_search_options(self, department_to_search: DropdownOption, item_type_to_search: DropdownOption):
        if department_to_search:
            logger.info(f"Adding Item Search Option: Department -> {department_to_search}")
            self.select_dropdown_option(
                locator_enum=ItemsMwsPageLocators.DEPARTMENT_DROPDOWN,
                dropdown_option=department_to_search
            )
        if item_type_to_search:
            logger.info(f"Adding Item Search Option: Item Type -> {item_type_to_search}")
            self.select_dropdown_option(
                locator_enum=ItemsMwsPageLocators.TYPE_DROPDOWN,
                dropdown_option=item_type_to_search
            )

    def _get_search_results(self) -> List[MwsItem]:
        results = []
        logger.info("Searching items...")
        try:
            self.wait_for_element_to_visible(element_to_wait_for=ItemsMwsPageLocators.RESULTS_ROWS)
            raw_results = self.find_elements(value_locator=ItemsMwsPageLocators.RESULTS_TABLE)
            for row in raw_results:
                row_values = self.get_values_from_row(row)
                results.append(MwsItem(
                    driver=self.driver,
                    plu=row_values[0],
                    description=row_values[1],
                    department=DropdownOption(row_values[2]),
                    unit_price=row_values[3])
                )
        except Exception as e:
            logger.exception(e)
        logger.info(f"Results count: {len(results)}")
        logger.info(f"Results info: {results}")
        return results

    def press_back(self):
        self.click(locator_enum=ItemsMwsPageLocators.BACK)
        self.click(locator_enum=MainMwsPageLocators.PROMPT_YES)

    def __save_button_enabler(self):
        # Sometimes button Save is not enabled even if all the information is valid.
        # In this scenario, activating a random element unlocks the button to Save the item.
        self.click(locator_enum=ItemsMwsPageLocators.TYPE_DROPDOWN)
        self.click(locator_enum=ItemsMwsPageLocators.TYPE_DROPDOWN)
