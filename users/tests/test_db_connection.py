import os
import sys
import django
from django.db import connections
from django.db.utils import OperationalError

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "microserviceForUserAuthenticationDjango.settings"
)
django.setup()


def check_database_connection():
    db_conn = connections["default"]
    try:
        db_conn.cursor()
        print("Successfully connected to the database.")
        return True
    except OperationalError:
        print("Failed to connect to the database.", file=sys.stderr)
        return False


if __name__ == "__main__":
    if check_database_connection():
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure
