import os
import sys

# Patch for old SQLite versions
try:
    import pysqlite3
    sys.modules["sqlite3"] = pysqlite3
except ImportError:
    pass

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webmdeditor.settings")

application = get_wsgi_application()
