#!/usr/bin/env bash
python ./manage.py collectstatic --noinput
python ./manage.py migrate --noinput
python ./manage.py qcluster &
python -m gunicorn --access-logfile - --access-logformat '%({X-Real-IP}i)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' --bind 0.0.0.0:6969 touhou_replay_database.wsgi
