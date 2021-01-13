#!/bin/sh

# wait for db init
python ./mysql_waiter.py

# Migrate / upgrade db
if [ "x$1" = "xtrue" ]; then
  flask db init -d "$SQLALCHEMY_MIGRATIONS_DIR"
  flask db migrate -d "$SQLALCHEMY_MIGRATIONS_DIR"
fi
flask db upgrade -d "$SQLALCHEMY_MIGRATIONS_DIR"

# Start gunicorn
exec gunicorn -b :5000 --workers 9 --threads 4 --timeout 90 --access-logfile - --error-logfile - ugmi:app