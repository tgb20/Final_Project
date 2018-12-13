# INFO 101 Final Project

# Notice
The github repo says it was created on 12/13, but that is because I accidently published a version with the database password still on it and I just recently noticed. The original repo was made public on 12/11.

# Live Demo
A live demo is available here: http://71.232.77.6:5000

# Requirements

To run this project you need to have Python 2.7 with the following libraries:

Flask - Runs python webserver
```
pip install flask
```

Py2Neo - Allows for interfacing with the Neo4J database
```
pip install py2neo
```

You will also need two Neo4J community edition databases, one running on port 7474 and the other running on 7473. Instructions on how to download, install, and setup Neo4J can be found [here](https://neo4j.com).


# How To Setup

Once you have all the requirements installed and your two Neo4J servers running you will need to edit the python scripts within the builders folder peoplelink.py, podcastlink.py, and databasepurger.py.

For the line
```
graph = Graph("http://neo4j:*password*@localhost:7474")
```

You will need to edit where it says *password* with the password you used to setup your Neo4J database.

After that is configured you can run the files with 
```
python podcastlink.py
python peoplelink.py
```

If you make changes to the data or screw up part of the database you can use databasepurger to clear the database, just make sure to change the port to the database you want to clear.

# Running the webserver

To run the webserver you need to setup the flask enviroment variable.
```
export FLASK_APP=link/to/webserver/main.py
```

In main.py of the webserver you will need to configure where the location of the static folder is. Change
```
webserverstatic = '/path/to/webserver/static/'
```
to have the correct location.

And then you can run the webserver with
```
python -m flask run
```
or
```
flask run
```

You should be able to navigate to the url it provides and experiment with queries.
