#!/usr/bin/env python
"""Django command-line utility for administrative tasks."""
import os
import sys

# Patch for old SQLite versions
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmdeditor.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldnt import Django. Are you sure its installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == "__main__":
    main()
