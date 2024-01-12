from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import Base, BaseOptions
from hornets.components.mws.mws_locators import ForecourtInstallationMwsPageLocators, MainMwsPageLocators


class MwsGrade(Base):

    def __init__(
            self,
            driver: WebDriver,
            grade_number,
            grade_name,
            grade_abbr,
            grade_low_product,
            grade_low_product_percent,
            grade_high_product,
            grade_high_product_percent,
    ):
        super().__init__(driver)
        self.grade_number = grade_number
        self.grade_name = grade_name
        self.grade_abbr = grade_abbr
        self.grade_low_product = grade_low_product
        self.grade_low_product_percent = grade_low_product_percent
        self.grade_high_product = grade_high_product
        self.grade_high_product_percent = grade_high_product_percent
        self.grade_options = MwsGradeOptions(driver)

    def edit_grade(self, grade_options: dict):
        self.grade_options.set_fields_value(grade_options)
        self.click(ForecourtInstallationMwsPageLocators.GRADE_SAVE_BUTTON)
        self.click(MainMwsPageLocators.SAVE_BUTTON)


class MwsGradeOptions(BaseOptions):

    def __init__(self, driver: WebDriver):
        fields = [
            ForecourtInstallationMwsPageLocators.GRADE_NAME,
            ForecourtInstallationMwsPageLocators.GRADE_REEFER,
            ForecourtInstallationMwsPageLocators.BLENDED_GRADE,
            ForecourtInstallationMwsPageLocators.LOW_PRODUCT,
            ForecourtInstallationMwsPageLocators.LOW_PRODUCT_PERCENT,
            ForecourtInstallationMwsPageLocators.HIGH_PRODUCT,
            ForecourtInstallationMwsPageLocators.HIGH_PRODUCT_PERCENT,
        ]
        super().__init__(driver, fields)
