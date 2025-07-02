#!/usr/bin/env bash
python ./manage.py collectstatic --noinput
python ./manage.py migrate --noinput
python ./manage.py qcluster &
python -m gunicorn --access-logfile - --bind 0.0.0.0:6969 touhou_replay_database.wsgi
