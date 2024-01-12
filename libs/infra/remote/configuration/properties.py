from typing import List
from typing import Optional
from typing import Union

from pydantic import BaseModel
from pydantic import Field


class ProviderProperties(BaseModel):
    url: str = Field(default=None)
    enabled: bool = Field(default=True)
    ignore_errors: bool = Field(default=False)

    @classmethod
    def load(cls, configs: Optional[dict]):
        if configs is not None:
            return cls(**configs)
        return None


class IpProperties(BaseModel):
    value: str
    type: str = Field(default="static")


class PortProperties(BaseModel):
    value: Union[int, str]
    type: str = Field(default="static")
    attr: str = Field(default=None)


class InstanceProperties(BaseModel):
    ip: IpProperties
    hostname: str = Field(default=None)
    port: PortProperties = Field(default=PortProperties(value=80, type='static'))
    homepage: str = Field(default="/")
    enabled: bool = Field(default=True)
    secure: bool = Field(default=False)

    @classmethod
    def load(cls, config: dict):
        config['ip'] = IpProperties(**config['ip'])
        if 'port' in config:
            config['port'] = PortProperties(**config['port'])
        return cls(**config)


class ServiceProperties(BaseModel):
    name: str
    enabled: bool = Field(default=True)
    description: str = Field(default=None)
    healthchecker: str = Field(default="@ping")
    instances: List[InstanceProperties] = Field(default=[])

    @classmethod
    def load(cls, raw_services: dict):
        services = []
        for name, config in raw_services.items():
            config['name'] = name
            config['instances'] = [InstanceProperties.load(instance) for instance in config['instances']]
            services.append(ServiceProperties(**config))
        return services
