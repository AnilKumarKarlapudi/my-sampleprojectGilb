import pytest

from hornets.components.mws.navigation_urls import (
    PDL_DOWNLOAD_PAGE_URL,
    ITEMS_PAGE_URL,
    STORE_CLOSE_PAGE_URL,
    TENDERS_PAGE_URL,
    LOYALTY_PAGE_URL,
    NETWORK_CONFIGURATION_PAGE_URL,
    REGISTERS_PAGE_URL
)


@pytest.fixture(scope="function")
def pdl_download_page(mws_go_to):
    pdl_download_page = mws_go_to(PDL_DOWNLOAD_PAGE_URL)
    yield pdl_download_page


@pytest.fixture(scope="class")
def items_page(mws_go_to):
    items_page = mws_go_to(ITEMS_PAGE_URL)
    yield items_page


@pytest.fixture(scope="class")
def store_close_page(mws_go_to):
    store_close_page = mws_go_to(STORE_CLOSE_PAGE_URL)
    yield store_close_page


@pytest.fixture(scope="class")
def tenders_page(mws_go_to):
    tenders_page = mws_go_to(TENDERS_PAGE_URL)
    yield tenders_page


@pytest.fixture(scope="class")
def loyalty_page(mws_go_to):
    loyalty_page = mws_go_to(LOYALTY_PAGE_URL)
    yield loyalty_page


@pytest.fixture(scope="class")
def site_configuration_page(mws_go_to):
    site_configuration_page = mws_go_to(NETWORK_CONFIGURATION_PAGE_URL)
    yield site_configuration_page


@pytest.fixture(scope="class")
def registers_page(mws_go_to):
    registers_page = mws_go_to(REGISTERS_PAGE_URL)
    yield registers_page
