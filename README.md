# GraduationThesis
require Python and JavaScript to run

# Open an cmd window in folder GraduationThesis:
## If you just start project, setup backend
```
cd backend
python>=3.9
pip install -r requirements.txt
```
`````
cd backend
`````
````
python manage.py makemigrations
`````
`````
python manage.py migrate
`````
`````
python manage.py createsuperuser
`````
`````
python manage.py runserver
`````

# Run Vue
### Open another tab of cmd:
`````
cd front-end
`````

`````
npm install
`````
Note: do not run npm audit fix or npm audit fix --fource, it will break the environment
`````
npm run server
`````


# setup Neo4j before start backend
Download Neo4j: Go to the [Neo4j Download Center](https://neo4j.com/deployment-center/) and download the Neo4j Desktop for macOS.

Install Neo4j: Open the downloaded file and follow the installation instructions.

Start Neo4j: Open Neo4j Desktop and create a new project. Start a new database and set the username to neo4j and password to 'Caoduy123'.