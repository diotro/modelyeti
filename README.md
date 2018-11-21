#### ModelYeti


##### Setup/Installation
```
cd /path/to/modelyeti

# create a virtual environment using python3.7
virtualenv venv --python=python3.7

# active the virtualenv
source venv/bin/activate

# install all dependencies 
pip3 install -r requirements.txt

# install the package locally, so that tests can access it
pip3 install -e src
```

You'll also need redis installed. See https://redis.io/topics/quickstart Then, run the server in
the background on port 14321 with:
```
redis-server --port 14321 --daemonize yes
```

Run the server with:
```
export FLASK_APP=src/yetiserver/app.py
flask run
```

Run the unit tests with:
```
python3 -m pytest test -k "not integration"
```