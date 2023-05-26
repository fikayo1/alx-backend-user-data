#!/usr/bin/env python3
"""
Filtered Logger module
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
     message: str, separator: str) -> str :
    """
    filter Datum function
    Args:
        fields: a list of strings representing all fields to obfuscate

        redaction: a string representing by what the field will be obfuscated

        message: a string representing the log line

        separator: a string representing by which character is separating all

    Returns:
        the log message obfuscated
    """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*{separator}",
                         f"{field}={redaction}{separator}", message)
    return message
