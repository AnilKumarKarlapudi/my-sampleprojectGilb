from pydantic import BaseModel
from pydantic import Field


# Default values for system user
DEFAULT_SYSTEM_USERNAME = "passporttech"
DEFAULT_SYSTEM_DOMAIN = "passport"
DEFAULT_SYSTEM_PASSWORD = "911Tech"


class SystemUser(BaseModel):
    """
    Platform (OS/Computer/Network) User
    """
    username: str = Field(default=DEFAULT_SYSTEM_USERNAME)
    domain: str = Field(default=DEFAULT_SYSTEM_DOMAIN)
    password: str = Field(default=DEFAULT_SYSTEM_PASSWORD)
