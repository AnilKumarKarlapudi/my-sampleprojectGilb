from hornets.models.speedkey import SpeedKey
from hornets.utilities.log_config import logger


# TODO
# This may be done in initial setup
# Delete last row of speedkeys
def test_prepare_last_row(speedkey_configuration_api):
    for i in range(13, 17):
        speedkey = SpeedKey(plu=f"{i}", caption=f"Speedkey {i}", position=i)
        if speedkey.exists(speedkey_configuration_api):
            logger.info(f"Speedkey in position {speedkey.position} was deleted. (cleaning last row)")
            speedkey.delete(speedkey_configuration_api)
        assert not speedkey.exists(speedkey_configuration_api)
    assert SpeedKey.count(speedkey_configuration_api) == 12


def test_create_delete_speed_key(speedkey_configuration_api, speedkey_14):
    initial_count = SpeedKey.count(speedkey_configuration_api)

    new_key = speedkey_14.save(speedkey_configuration_api)

    assert new_key == speedkey_14

    assert SpeedKey.count(speedkey_configuration_api) > initial_count

    new_key.delete(speedkey_configuration_api)

    assert SpeedKey.count(speedkey_configuration_api) == initial_count


def test_create_delete_multiple_speed_key(speedkey_configuration_api, speedkey_14, speedkey_13):
    initial_count = SpeedKey.count(speedkey_configuration_api)

    new_key = speedkey_14.save(speedkey_configuration_api)

    assert new_key == speedkey_14

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 1

    new_key = speedkey_13.save(speedkey_configuration_api)

    assert new_key == speedkey_13

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 2

    speedkey_13.delete(speedkey_configuration_api)

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 1

    speedkey_14.delete(speedkey_configuration_api)

    assert SpeedKey.count(speedkey_configuration_api) == initial_count


def test_exists_speed_key(speedkey_configuration_api, speedkey_14, speedkey_13):
    initial_count = SpeedKey.count(speedkey_configuration_api)

    new_key = speedkey_14.save(speedkey_configuration_api)

    assert new_key == speedkey_14

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 1

    new_key = speedkey_13.save(speedkey_configuration_api)

    assert new_key == speedkey_13

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 2

    speedkey_13.delete(speedkey_configuration_api)

    assert SpeedKey.count(speedkey_configuration_api) == initial_count + 1

    speedkey_14.delete(speedkey_configuration_api)

    assert SpeedKey.count(speedkey_configuration_api) == initial_count
