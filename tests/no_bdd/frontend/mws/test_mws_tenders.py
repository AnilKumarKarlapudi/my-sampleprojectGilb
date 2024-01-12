import os
import pytest
import random

from hornets.base import DropdownOption
from hornets.components.mws.mws_locators import TendersMwsPageLocators
from hornets.models.tender.enums import (
    TenderGroupEnum,
    NacsTenderCodeEnum,
    SecondaryTenderForChangeEnum,
)


@pytest.mark.mws
@pytest.mark.tenders
class TestEditTenders:
    def test_edit_tender(self, tenders_page):
        random_description = f"Test Edit {random.randint(0, 1000)}"
        new_edit_data = {
            TendersMwsPageLocators.TENDER_GROUP: DropdownOption("Cash"),
            TendersMwsPageLocators.TENDER_RECEIPT_DESCRIPTION: random_description,
            TendersMwsPageLocators.TENDER_BUTTON_DESCRIPTION: "Test",
            TendersMwsPageLocators.NACS_TENDER_CODE: DropdownOption("coupons"),
            TendersMwsPageLocators.PRIMARY_TENDER_FOR_CHANGE: DropdownOption("Other"),
            TendersMwsPageLocators.SECONDARY_TENDER_FOR_CHANGE: DropdownOption("Other"),
        }

        tenders_page.edit_tender(tender_code="5", values_to_edit=new_edit_data)

        current_tender = tenders_page.get_tender(tender_code="5")
        current_tender_options = current_tender.get_tender_options()

        assert current_tender_options[TendersMwsPageLocators.TENDER_GROUP] == DropdownOption("Cash")

        assert current_tender_options[TendersMwsPageLocators.TENDER_RECEIPT_DESCRIPTION] == random_description
        assert current_tender_options[TendersMwsPageLocators.TENDER_BUTTON_DESCRIPTION] == "Test"
        assert current_tender_options[TendersMwsPageLocators.NACS_TENDER_CODE] == DropdownOption("coupons")


@pytest.mark.tenders
class TestAddTenders:

    @pytest.mark.skipif(os.getenv("environment") == "local",
                        reason="We skip the test if we are running on local environment to avoid overloading "
                               "our local configurations, since tenders cannot be deleted.")
    def test_add_tender(self, tenders_page):
        new_tender_data = {
            TendersMwsPageLocators.TENDER_DESCRIPTION: "Test Add",
            TendersMwsPageLocators.TENDER_CODE: str(random.randint(9, 999)),
            TendersMwsPageLocators.TENDER_GROUP: TenderGroupEnum.LOCAL_ACCOUNTS,
            TendersMwsPageLocators.TENDER_RECEIPT_DESCRIPTION: "Test Add",
            TendersMwsPageLocators.TENDER_BUTTON_DESCRIPTION: "Test",
            TendersMwsPageLocators.NACS_TENDER_CODE: NacsTenderCodeEnum.COUPONS,
            TendersMwsPageLocators.SECONDARY_TENDER_FOR_CHANGE: SecondaryTenderForChangeEnum.NO_TENDER,
        }

        tenders_page.add_tender(new_tender_data)

        new_tender = tenders_page.get_tender(tender_code=new_tender_data[TendersMwsPageLocators.TENDER_CODE])

        assert new_tender.tender_description == new_tender_data[TendersMwsPageLocators.TENDER_DESCRIPTION]
        assert new_tender.code == new_tender_data[TendersMwsPageLocators.TENDER_CODE]
