import time

from typing import Union


# Classic utilities


def compare_instances(instance_1, instance_2):
    """
    Compare two instances for equality.

    Parameters:
    - instance_1: The first instance for comparison.
    - instance_2: The second instance for comparison.

    Returns:
    True if instances are equal, False otherwise.
    """
    if not isinstance(instance_1, instance_2.__class__):
        return False
    for key, value in instance_2.__dict__.items():
        if value != getattr(instance_1, key):
            return False

    return True


# Casters


def default_caster(input):
    """
    Default caster function.

    Parameters:
    - input: The input value to be casted.

    Returns:
    The input value unchanged.
    """
    return input


def wait(seconds: Union[int, float]):
    """
    Sleeps for given seconds.

    :param seconds: Union[int, float] - seconds to wait
    """
    time.sleep(seconds)


class Timeout:
    """
    Timeout handler.
    """

    @staticmethod
    def wait(seconds: Union[int, float]):
        """
        Sleeps for given seconds.
        """
        wait(seconds)

    def __init__(self, seconds: Union[int, float]):
        """
        Constructor
        """
        self._seconds = seconds
        self._start_at = time.time()

    def is_timeout(self, fail: bool = False) -> bool:
        """
        Check if it's timeout

        :param fail: bool - if set to true, a TimeoutError will be raised
        :raise TimeoutError: on timeout and fail flag set to true
        :return: bool - is timeout?
        """
        is_timeout = time.time() > self._start_at + self._seconds
        if is_timeout and fail:
            raise TimeoutError()
        return is_timeout
