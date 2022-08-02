# -*- coding: utf-8 -*-

"""
Copyright (c) Microsoft Corporation and Dapr Contributors.
Licensed under the MIT License.
"""

import re
from datetime import timedelta

# Regex to parse Go Duration datatype, e.g. 4h15m50s
DAPR_DURATION_PARSER = re.compile(r'((?P<hours>\d+)h)?((?P<mins>\d+)m)?((?P<seconds>\d+)s)?$')


def convert_from_dapr_duration(duration: str) -> timedelta:
    """Converts Dapr duration format (Go duration format) to datetime.timedelta.

    Args:
        duration (str): Dapr duration string.

    Returns:
        :obj:`datetime.delta`: the python datetime object.
    """

    matched = DAPR_DURATION_PARSER.match(duration)
    if not matched or matched.lastindex == 0:
        raise ValueError(f'Invalid Dapr Duration format: \'{duration}\'')

    days = 0.0
    hours = 0.0

    if matched.group('hours') is not None:
        days, hours = divmod(float(matched.group('hours')), 24)
    mins = float(matched.group('mins')) if matched.group('mins') else 0.0
    seconds = float(matched.group('seconds')) if matched.group('seconds') else 0.0

    return timedelta(
        days=days,
        hours=hours,
        minutes=mins,
        seconds=seconds)


def convert_to_dapr_duration(td: timedelta) -> str:
    """Converts date.timedelta to Dapr duration format.

    Args:
        td (datetime.timedelta): python datetime object.

    Returns:
        str: dapr duration format string.
    """

    total_minutes, secs = divmod(td.total_seconds(), 60.0)
    hours, mins = divmod(total_minutes, 60.0)

    return f'{hours:.0f}h{mins:.0f}m{secs:.0f}s'
