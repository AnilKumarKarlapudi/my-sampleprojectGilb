import json
from datetime import datetime
from typing import IO

from playhouse.shortcuts import model_to_dict

from libs.infra.remote.configuration.configurator import Configurator
from libs.infra.remote.models import Instance


def loads(io_config: IO):
    """
    Loads configuration from an IO file.

    :param io_config: IO configuration file
    """
    configurator = Configurator(io_config)
    configurator.cleanup()
    configurator.configure()


def report(fp_report: IO):
    """
    Generates a JSON file with the list of instances persisted.

    :param fp_report: IO file
    """
    instances = []
    for instance in Instance.select().execute():
        instances.append(model_to_dict(instance))
    json.dump(instances, fp_report, indent=4, default=_json_serializer)
    fp_report.close()


def _json_serializer(obj):
    """

    :param obj:
    :return:
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
