from libs.common.enums import InterfaceEnum


class ExtractionToolSection(InterfaceEnum):
    TAXES = (0, "Taxes")
    DISCOUNTS = (1, "Discounts")
    ITEMS = (2, "Items")
    DEPARTMENTS = (3, "Departments")
    REGISTER_GROUPS = (4, "Register Groups")
    SPEED_KEYS = (5, "Speed Keys")
    DEPARTMENT_KEYS = (6, "Department Keys")
    STORE_OPTIONS = (7, "Store Options")
    ACCOUNTING_OPTIONS = (8, "Accounting Options")
    TENDER_KEYS = (9, "Tender Keys")
    LOCAL_ACCOUNTS = (10, "Local Accounts")
    PAID_IN_PAID_OUT = (11, "Paid In Paid Out")
    PERIOD_MAINTENANCE = (12, "Period Maintenance")
    SECURITY_GROUPS = (13, "Security Groups")
    REASON_CODES = (14, "Reason Codes")
    CARWASH_PROGRAMMING = (15, "Carwash Programming")
    LOYALTY_INTERFACE = (16, "Loyalty Interface")
    REMINDER_MAINTENANCE = (17, "Reminder Maintenance")
    CRIND_MERCHANDISING = (18, "Crind Merchandising")
    THIRD_PARTY_DATA_INTERFACE = (19, "Third Party Data Interface")
    REPORT_MAINTENANCE = (20, "Report Maintenance")
    BACK_OFFICE_INTERFACE_OPTIONS = (21, "Back Office Interface Options")
    FORECOURT_INSTALLATION = (22, "Forecourt Installation")


class ExtractionToolCategory(InterfaceEnum):
    PRICE_BOOK = (0, "Price Book")
    REGISTER = (1, "Register")
    STORE = (2, "Store")
    SITE_SPECIFIC_DATA = (3, "Site Specific Data")
    FUEL = (4, "Fuel")


ALL_SECTIONS_BACKEND = [section.backend for section in ExtractionToolSection]
ALL_SECTIONS_FRONTEND = [section.frontend for section in ExtractionToolSection]
