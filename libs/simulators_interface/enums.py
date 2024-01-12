from enum import Enum


class SimulatorResource(Enum):
    PINPAD = "Pinpad"
    CRIND = "crindsim"


class PinpadSimMode(Enum):
    AUTO = "Auto"
    MANUAL = "Manual"


class CrindSimMode(Enum):
    AUTO = "auto"
    MANUAL = "manual"
