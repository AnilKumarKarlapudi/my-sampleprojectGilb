from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import Model

from libs.infra.remote.persistence import get_connection


class Service(Model):
    """
    Service object class
    """

    class Meta:
        database = get_connection()

    # Name
    name = CharField(primary_key=True)

    # Is enabled
    enabled = BooleanField(default=True)

    # Description
    description = CharField(max_length=128, null=True)

    # Health Checker
    healthchecker = CharField(max_length=253, null=False)

    # TODO: implement subscriptions
    # Started at
    started_at = DateTimeField(default=lambda: datetime.now())

    # TODO: implement health checker
    # Last update at
    last_update_at = DateTimeField(null=True, default=lambda: datetime.now())
