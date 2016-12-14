# Buy Rent Sell
A social ecommerce platform allowing users to buy, rent, and sell items. 

## Development Setup

```
# Install Anaconda
$ pip3 install anaconda
```

```
# Create environment directory
$ conda create -n brs flask python=3.5
$ cd anconda3/envs/brs

# start virtual environment
$ source activate brs
```

# Install additional Packages
```
$ conda install -c conda-forge flask-sqlalchemy=2.1
$ conda install sqlalchemy 
$ conda install psycopg2
$ conda install flask-login
$ conda install flask-admin
```

# Retrieve our project and get it running
```
$ git clone https://github.com/mhendri/buyrentsell
$ cd brs
```

# Create our database based off our model, run the following commands
```
$ python
>>> from app import db
>>> db.create_all()
>>> exit()
```

# Get the app running locally
```
$ export FLASK_APP=app.py
$ flask run
```
