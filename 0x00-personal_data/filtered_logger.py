#!/usr/bin/env python3
"""
filtered_logger module
"""
import logging
from os import getenv
import re
from typing import List, Tuple

import mysql.connector

PII_FIELDS: Tuple = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Filter values in incoming log records.
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


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


def get_logger() -> logging.Logger:
    """
    Returns a Logger object."""
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a DB connector."""
    host: str = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db: str = getenv('PERSONAL_DATA_DB_NAME')
    usr: str = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    pwd: str = getenv('PERSONAL_DATA_DB_PASSWORD', '')

    return mysql.connector.connect(host=host, database=db,
                                   user=usr, password=pwd)


def main():
    """
    Main handler.
    Filters rows from the db."""
    conn = get_db()
    cursor = conn.cursor()
    logger = get_logger()
    cols = ['name', 'email', 'phone', 'ssn',
            'password', 'ip', 'last_login', 'user_agent']
    cursor.execute("SELECT * FROM users;")
    for row in cursor:
        msg = ""
        for name, value in zip(cols, row):
            msg += '{}={};'.format(name, value)
        logger.info(msg)

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
