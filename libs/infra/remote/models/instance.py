from hashlib import sha512

from peewee import BooleanField
from peewee import CharField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Model

from libs.infra.remote.models.service import Service
from libs.infra.remote.persistence import get_connection


class Instance(Model):
    """
    Instance object class
    """

    class Meta:
        database = get_connection()

    # Identifier
    identifier = CharField(primary_key=True, unique=True)

    # IP
    ip = CharField(max_length=15)

    # Hostname
    hostname = CharField(max_length=253)

    # Port
    port = IntegerField(default=80)

    # Is secure?
    secure = BooleanField(default=False)

    # Is enabled?
    enabled = BooleanField(default=True)

    # Homepage
    homepage = CharField(default=None, null=True)

    # Service
    service = ForeignKeyField(Service, backref='instances')

    def get_identifier(self):
        assert self.service is not None
        assert self.ip and self.ip != ""
        assert self.hostname and self.hostname != ""
        assert self.port and self.port > 0

        tokens = [self.service.name, self.ip, self.hostname, str(self.port)]
        hashed = sha512(b"")
        for token in tokens:
            hashed.update(token.encode('utf-8'))
        return hashed.hexdigest()

    def generate(self) -> str:
        # HTTP schema
        schema = "https" if self.secure else "http"

        # Host
        host = self.ip if self.ip == self.hostname or not self.hostname else self.hostname

        port = str(self.port)

        return f"{schema}://{host}:{port}"
