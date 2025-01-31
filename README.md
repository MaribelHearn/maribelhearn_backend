# Maribel Hearn's Web Portal - Database
This is the database used to store the Touhou world records and Lunatic no miss no bomb runs that are available at [maribelhearn.com](https://maribelhearn.com).
See the [repository](https://github.com/MaribelHearn/maribelhearn.com) for the website frontend.

The database is built using [Django](https://docs.djangoproject.com/) and it allows for managing the Touhou runs stored for the website.
Users may add, update, and remove WR runs and LNN runs, as well as upload replay files for them. These replays are stored in the `media` directory.

## How to run
Prerequisites:
* Python
* MariaDB
* The maribelhearn.com repository

### Cloning the repository
First, clone the repository in whatever way you prefer and navigate to its directory.
```
git clone https://github.com/MaribelHearn/maribelhearn_backend.git
cd maribelhearn_backend
```

### Installing the requirements
Set up a virtual environment for Python 3.10.14. This can be conveniently handled by a tool such as [pyenv](https://github.com/pyenv/pyenv-virtualenv).
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

### Setting up the environment
Create an environment file called `django_env` based on `django_env.template`. Fill out your PYTHONPATH, your database credentials, and the directory that you cloned the maribelhearn.com repository to.

In the `touhou_replay_database` directory, adjust the values in the `settings.py` file to your liking. This includes the key used for Django and the port that gunicorn will run on.

### Running gunicorn and qcluster
After installing the requirements, make sure these two programs are running. On Linux, you could set up systemd services to have them running in the background.
Make sure that the `django_env` environment file is loaded when running gunicorn and qcluster, no matter in which way they are run. Run both programs using the Python version from your virtual environment.
```
gunicorn --access-logfile --bind 127.0.0.1:<YOUR_PORT_HERE> touhou_replay_database.wsgi
python ./manage.py qcluster
```
Once both are running, access the database at http://localhost:<YOUR_PORT_HERE> and log in with your database credentials.
