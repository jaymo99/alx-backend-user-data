#!/usr/bin/env python3
"""
filtered_logger module
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates a log message.

    Args:
        fields: list of strings representing all fields to obfuscate.
        redaction: a string representing by what the field will be obfuscated.
        message: a string representing the log line
        separator: a string representing by which character is separating
            all fields in the log line.

    Returns:
        The log message obfuscated.
    """
    return re.sub(
        r'({})=([^{}]*)'.format('|'.join(fields), separator),
        r'\1={}'.format(redaction),
        message
        )
