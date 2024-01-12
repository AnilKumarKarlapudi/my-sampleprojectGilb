from typing import Callable


class NetworkHandler(object):
    """
    Network Handler object
    """
    def __init__(self):
        self._initialized = False

    def init(self) -> bool:
        """
        Network initialization implementation
        """
        has_initialized = False
        if not self._initialized:
            self._init()
            self._initialized = True
            has_initialized = True
        return has_initialized

    def filterer(self) -> Callable[[str], bool]:
        """
        Network message body filterer
        """
        raise NotImplementedError("Network handler needs to be implemented!")

    def _init(self):
        """
        Network custom implementation of initialization
        """
        raise NotImplementedError("Network handler needs to be implemented!")
