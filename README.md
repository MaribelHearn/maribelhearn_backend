# Maribel Hearn's Web Portal - Backend
This is the backend used to manage the Touhou world records and Lunatic no miss no bomb runs that are available at [maribelhearn.com](https://maribelhearn.com).
See the [repository](https://github.com/MaribelHearn/maribelhearn.com) for the website frontend.

The backend is built using [Django](https://docs.djangoproject.com/) and it allows for managing the Touhou runs stored for the website.
Users may add, update, and remove WR runs and LNN runs, as well as upload replay files for them. These replays are stored in the `media` directory.

## How to run
First, clone the repository in whatever way you prefer and navigate to its directory.
```
git clone https://github.com/MaribelHearn/maribelhearn_backend.git
cd maribelhearn_backend
```
Use the Dockerfile provided in the repository to build a [Docker image](https://docs.docker.com/).

Create an environment file called `django_env` based on `django_env.production` and fill out any necessary variables.
The defaults can be found in `settings.py` in the `touhou_replay_database` directory.

In the repository's parent directory, you may use a Docker Compose file:
```YAML
mh_backend:
  image: mh_backend
  container_name: mh_backend
  restart: 'unless-stopped'
  depends_on:
    - mariadb
    - redis
  volumes:
    - ./mh_backend:/app
    - ./mh_backend/static:/app/static
    - ./mh_backend/media:/app/media
  ports:
    - <your_port_here>:6969
  env_file:
    - ./mh_backend/django_env
```

## Running without Docker
Prerequisites:
* Python
* MariaDB
* Redis
* The maribelhearn.com repository

### Installing the requirements
Once you have cloned the repository, set up a virtual environment for Python 3.10.14. This can be conveniently handled by a tool such as [pyenv](https://github.com/pyenv/pyenv-virtualenv).
Give it in any name you like. In this example, the virtual environment is named `db`.
```
pyenv install 3.10.14
pyenv virtualenv 3.10.14 db
```
Next, install the requirements using [pip](https://pypi.org/project/pip/). Make sure to run pip using the Python version from your virtual environment.
```
pip install -r requirements.txt
```
This will also install `gunicorn` and `qcluster`. Gunicorn is responsible for running the database, while QCluster is used for webhook support.
Make sure [MariaDB](https://mariadb.org/) and [Redis](https://redis.io/) are running on your system. You may refer to their websites for more information.

### Setting up the environment
Create an environment file called `django_env` based on `django_env.development`. Fill out your PYTHONPATH and your database credentials.

In the `touhou_replay_database` directory, adjust the values in the `settings.py` file to your liking. This includes the key used for Django and the port that gunicorn will run on.

### Running gunicorn and qcluster
After installing the requirements, make sure these two programs are running. On Linux, you could set up systemd services to have them running in the background.
Make sure that the `django_env` environment file is loaded when running gunicorn and qcluster, no matter in which way they are run. Run both programs using the Python version from your virtual environment.
```
python ./manage.py collectstatic --noinput
python ./manage.py migrate --noinput
python ./manage.py qcluster
python -m gunicorn --access-logfile --bind 127.0.0.1:<YOUR_PORT_HERE> touhou_replay_database.wsgi
```
Change 127.0.0.1 to 0.0.0.0 if you are running behind a reverse proxy on a different machine.

Once both are running, access the database at http://localhost:<YOUR_PORT_HERE> and log in with your database credentials.
