#!/usr/bin/env python3
"""Filtered Logger."""
from typing import List
import re
import logging
from logging import StreamHandler
import os
from mysql.connector import connect, MySQLConnection

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
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

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record."""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """Create a logger."""
    logger = logging.getLogger(name="user_data")
    logger.setLevel(logging.INFO)
    handler = StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Redact sensitive fields from data."""
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


def get_db() -> MySQLConnection:
    """Connect to the database."""
    return connect(user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
                   password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
                   host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
                   database=os.getenv("PERSONAL_DATA_DB_NAME", "holberton"))


def main():
    """Display all rows in the database."""
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        logger.info(
            " ".join([f"{key}={value};" for key, value in row.items()])
        )


if __name__ == '__main__':
    main()
    

