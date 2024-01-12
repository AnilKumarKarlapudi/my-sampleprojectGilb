import os
import random
from datetime import datetime

import pytest
from grpc import Channel
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService

from hornets.components.mws.navigation_urls import POS_PAGE_URL
from hornets.components.pos.pos import Pos

from hornets.models.manual_discount.models import ManualDiscount
from hornets.models.manual_discount.enums import ManualDiscountMethod, ManualDiscountReason
from hornets.models.register.models import Register

from hornets.tools.extraction.tool import ExtractionTool

from hornets.utilities.log_config import logger
from hornets.utilities.constants import (
    CHROME_WEBDRIVER_EXECUTABLE,
    CHROME_SELECTORS_HUB_EXTENSION,
    MAX_IMPLICIT_TIME_TO_WAIT,
)

from libs.grpc.api.employee import EmployeeAPI
from libs.grpc.api.extraction_tool import ExtractionToolAPI
from libs.grpc.api.manual_discount import ManualDiscountAPI
from libs.grpc.api.register import RegisterAPI
from libs.grpc.api.speedkey import SpeedKeyAPI
from libs.grpc.connector.main import MwsGRPC
from libs.grpc.connector.ports import PassportServices
from libs.grpc.services.models import GrpcApiChannel, GrpcToolChannel


# Pytest will look into these modules to discover common fixtures and step definitions, without the
# need to import them. They will be available as if they were inside a conftest.py file.
pytest_plugins = [
    "tests.bdd.step_defs.catalog.mws_step_catalog_definitions",
    "tests.bdd.step_defs.catalog.pos_step_catalog_definitions",
    "tests.mws_navigation",
]


# Definition of command line arguments
def pytest_addoption(parser):
    parser.addoption(
        "--environment",
        action="store",
        default="local",
        help="Indicates if we are running the project in a local environment or in a CI/CD server. "
             "Options: [local, cicd]"
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"reports/report_{timestamp}.html"
    os.environ["environment"] = config.getoption("environment")


"""
@pytest.fixture(scope="function")
def last_known_message():
    yield NetworkMessageService().get_last_network_message()


@pytest.fixture(scope="function")
def message_validator(last_known_message):
    def _message_validator(message_checker_func):
        return NetworkMessageService().wait_for_network_message(
            message_checker=message_checker_func, last_message_id=last_known_message.network_message_id, timeout=5
        )

    yield _message_validator
"""


@pytest.fixture(scope="class")
def driver() -> WebDriver:
    logger.info("Initializing Chrome driver")
    service = ChromeService(executable_path=CHROME_WEBDRIVER_EXECUTABLE)
    options = webdriver.ChromeOptions()
    options.add_extension(CHROME_SELECTORS_HUB_EXTENSION)
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(time_to_wait=MAX_IMPLICIT_TIME_TO_WAIT)
    yield driver
    driver.quit()


@pytest.fixture(scope="class")
def pos(driver) -> Pos:
    driver.get(POS_PAGE_URL)
    pos = Pos(driver)
    yield pos


# GRPC Channels
@pytest.fixture(scope="class")
def grpc_configuration_channel() -> Channel:
    grpc_connector = MwsGRPC()
    logger.info("Get configuration channel for api calls")
    yield grpc_connector.create_channel(port=PassportServices.CONFIGURATION.value)


# GRPC APIs
@pytest.fixture(scope="class")
def manual_discount_configuration_api(grpc_configuration_channel) -> GrpcApiChannel:
    yield ManualDiscountAPI(grpc_configuration_channel)


@pytest.fixture(scope="class")
def speedkey_configuration_api(grpc_configuration_channel) -> GrpcApiChannel:
    yield SpeedKeyAPI(grpc_configuration_channel)


@pytest.fixture(scope="class")
def employee_configuration_api(grpc_configuration_channel) -> GrpcApiChannel:
    yield EmployeeAPI(grpc_configuration_channel)


@pytest.fixture(scope="class")
def register_configuration_api(grpc_configuration_channel) -> GrpcApiChannel:
    yield RegisterAPI(grpc_configuration_channel)


@pytest.fixture(scope="class")
def extraction_tool_configuration_api(grpc_configuration_channel) -> GrpcToolChannel:
    yield ExtractionToolAPI(grpc_configuration_channel)


@pytest.fixture(scope="class")
def extraction_tool(extraction_tool_configuration_api) -> ExtractionTool:
    yield ExtractionTool(backend_api=extraction_tool_configuration_api)


# Factories
@pytest.fixture(scope="function")
def manual_discount_factory(request, manual_discount_configuration_api):
    def _manual_discount_factory(
        discount_name: str = None,
        discount_method: ManualDiscountMethod = None,
        discount_reason: ManualDiscountReason = None,
        amount: float = None,
        force_delete: bool = True,
    ):
        """
        Creates a discount with the given parameters and deletes it (if force_delete is True)
        """

        discount = ManualDiscount(
            name=discount_name or f"DISCOUNT_{random.randint(0, 100000)}",
            method=discount_method or ManualDiscountMethod.ITEM_AMOUNT_OFF,
            reason=discount_reason or ManualDiscountReason.MANAGERS_GOODWILL,
            amount=amount or 10.00,
        )

        def _delete_manual_discount():
            if force_delete:
                logger.info(f"Deleting discount {discount.name}")
                discount.delete(manual_discount_configuration_api)

        request.node.addfinalizer(_delete_manual_discount)
        logger.info(f"Creating discount {discount.name}")
        return discount.save(manual_discount_configuration_api)

    yield _manual_discount_factory


@pytest.fixture(scope="function")
def register_factory(request, register_configuration_api):
    def _register_factory(
        force_delete: bool = True,
        save_model: bool = True,
        **kwargs
    ):
        """
        Creates a register with the given parameters and deletes it (if force_delete is True)
        """
        register_kwargs = kwargs

        # Use received ID or create a random one
        if 'id' in kwargs:
            register_id = register_kwargs['id']
            register_kwargs.pop('id')
        else:
            register_id = random.randint(50, 97)  # Valid ID range is 1-97, use above 50 to find an unused one

        register = Register(
            id=register_id,
            **register_kwargs
        )

        def _delete_register():
            if force_delete:
                logger.info(f"Deleting register {register.id}")
                register.delete(register_configuration_api)

        request.node.addfinalizer(_delete_register)
        logger.info(f"Creating register {register.id}")

        if save_model:
            return register.save(register_configuration_api)
        else:
            return register

    yield _register_factory
