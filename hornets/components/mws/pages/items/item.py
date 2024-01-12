from collections import namedtuple

from selenium.webdriver import ActionChains, Keys

from hornets.base import Base
from hornets.components.mws.mws_locators import ItemsMwsPageLocators
from hornets.components.mws.pages.items.items_options import ItemOptions
from hornets.components.mws.pages.items.items_enums import ItemTypeEnum


class MwsItem(Base):

    def __init__(
            self,
            driver,
            plu,
            description,
            department,
            item_type=ItemTypeEnum.REGULAR_ITEM,
            price_required=False,
            price_option=1,
            unit_price=None,
            deal_quantity=None,
            deal_price=None
    ):
        super().__init__(driver)
        self.plu = plu
        self.description = description
        self.department = department
        self.item_type = item_type
        self.price_required = price_required
        self.price_option = price_option
        self.unit_price = unit_price
        self.deal_quantity = deal_quantity
        self.deal_price = deal_price
        self.item_options = ItemOptions(driver=driver)

    def edit(self, options_to_edit):
        self.item_options.set_fields_value(fields_value=options_to_edit)

    def get_options(self):
        return self.item_options.fields

    def set_price_option(
            self,
            price_option: int,
            unit_price: float = None,
            deal_quantity: int = None,
            deal_price: float = None
    ):
        PriceOptionLocators = namedtuple(
            typename="PriceOption",
            field_names="radio_locator, unit_price_locator, deal_quantity_locator, deal_price_locator"
        )
        price_option_1 = PriceOptionLocators(
            radio_locator=ItemsMwsPageLocators.NORMAL_PRICE_RADIO,
            unit_price_locator=ItemsMwsPageLocators.NORMAL_PRICE_INPUT,
            deal_quantity_locator=None,
            deal_price_locator=None
        )

        price_option_2 = PriceOptionLocators(
            radio_locator=ItemsMwsPageLocators.BASE_PLUS_ONE_RADIO,
            unit_price_locator=ItemsMwsPageLocators.BASE_PLUS_ONE_UNITPRICE_INPUT,
            deal_quantity_locator=ItemsMwsPageLocators.BASE_PLUS_ONE_DEALQUANTITY_INPUT,
            deal_price_locator=None
        )

        price_option_3 = PriceOptionLocators(
            radio_locator=ItemsMwsPageLocators.GROUP_THRESHOLD_RADIO,
            unit_price_locator=ItemsMwsPageLocators.GROUP_THRESHOLD_UNITPRICE_INPUT,
            deal_quantity_locator=ItemsMwsPageLocators.GROUP_THRESHOLD_DEALQUANTITY_INPUT,
            deal_price_locator=ItemsMwsPageLocators.GROUP_THRESHOLD_DEALPRICE_INPUT
        )

        price_option_4 = PriceOptionLocators(
            radio_locator=ItemsMwsPageLocators.BULK_RADIO,
            unit_price_locator=None,
            deal_quantity_locator=ItemsMwsPageLocators.BULK_DEALQUANTITY_INPUT,
            deal_price_locator=ItemsMwsPageLocators.BULK_DEALPRICE_INPUT
        )

        price_option_5 = PriceOptionLocators(
            radio_locator=ItemsMwsPageLocators.UNIT_ADJUSTED_RADIO,
            unit_price_locator=ItemsMwsPageLocators.UNIT_ADJUSTED_UNITPRICE_INPUT,
            deal_quantity_locator=ItemsMwsPageLocators.UNIT_ADJUSTED_DEALQUANTITY_INPUT,
            deal_price_locator=ItemsMwsPageLocators.UNIT_ADJUSTED_DEALPRICE_INPUT
        )

        price_option_mapping = {
            1: price_option_1,
            2: price_option_2,
            3: price_option_3,
            4: price_option_4,
            5: price_option_5,
        }

        selected_option = price_option_mapping[price_option]

        self.click(locator_enum=selected_option.radio_locator)

        self.price_option = price_option
        self.item_options.fields[selected_option.radio_locator] = True

        price_inputs = []

        if selected_option.unit_price_locator and unit_price:
            price_inputs.append(self.find_element(value_locator=selected_option.unit_price_locator))
            self.clear_and_set_value(
                locator_enum=selected_option.unit_price_locator,
                value=str(unit_price),
                force_clear=True
            )
            self.unit_price = unit_price
            self.item_options.fields[selected_option.unit_price_locator] = str(unit_price)

        if selected_option.deal_quantity_locator and deal_quantity:
            price_inputs.append(self.find_element(value_locator=selected_option.deal_quantity_locator))
            self.clear_and_set_value(
                locator_enum=selected_option.deal_quantity_locator,
                value=str(deal_quantity),
                force_clear=True
            )
            self.deal_quantity = deal_quantity
            self.item_options.fields[selected_option.deal_quantity_locator] = str(deal_quantity)

        if selected_option.deal_price_locator and deal_price:
            price_inputs.append(self.find_element(value_locator=selected_option.deal_price_locator))
            self.clear_and_set_value(
                locator_enum=selected_option.deal_price_locator,
                value=str(deal_price),
                force_clear=True
            )
            self.deal_price = deal_price
            self.item_options.fields[selected_option.deal_quantity_locator] = str(deal_price)

        # Without pressing Enter Key after completing data in these inputs the validations will not go away
        # and the button Save will not be active, even if the data is valid.
        for price_input in price_inputs:
            price_input.click()
            ActionChains(self.driver).pause(1).send_keys(Keys.ENTER).perform()

    def __str__(self):
        return (
            f"Item: "
            f"[PLU={self.plu}, "
            f"Description={self.description}, "
            f"Department={self.department.locator_value}"
            f"Type={self.item_type.value}]"
        )
