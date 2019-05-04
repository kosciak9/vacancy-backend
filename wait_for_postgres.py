import logging
import os
from time import sleep, time

import psycopg2

CHECK_TIMEOUT = int(os.getenv("POSTGRES_CHECK_TIMEOUT", "30"))
CHECK_INTERVAL = int(os.getenv("POSTGRES_CHECK_INTERVAL", "1"))
INTERVAL_UNIT = "second" if CHECK_INTERVAL == 1 else "seconds"
CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "vacancy"),
    "user": os.getenv("POSTGRES_USER", "vacancy"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
    "host": os.getenv("DATABASE_URL", "vacancy_db")
}

START_TIME = time()
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(logging.StreamHandler())


def pg_isready(host, user, password, dbname):
    """
    Function that pings Postgres database to check if it's online
    """
    while time() - START_TIME < CHECK_TIMEOUT:
        try:
            conn = psycopg2.connect(**vars())
            LOGGER.info("Postgres is ready!")
            conn.close()
            return True
        except psycopg2.OperationalError:
            LOGGER.info("Postgres isn't ready. "
                        f"Waiting for {CHECK_INTERVAL} {INTERVAL_UNIT}...")
            sleep(CHECK_INTERVAL)

    LOGGER.error(f"We could not connect to Postgres within {CHECK_TIMEOUT} seconds.")
    return False


pg_isready(**CONFIG)
