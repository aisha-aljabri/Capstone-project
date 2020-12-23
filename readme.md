Capstone project

# Getting Setup
Installing Dependencies:
- Python 3.7
- in the project root running:
    pip install -r requirements.txt

Environment Variables:
- in the models.py file Replace database_path with your database information

Running the server: 
To run the server, execute:
- FLASK_APP=app.py flask run


# Casting Agency Specifications
Models:
- there are two models
1- Actor with attribute:
   - name
   - age
   - gender
2- Movie with attribute:
   - title
   - release_date
   - genre

JWT token:
- in the .env file, there are three JWT token:
   1- CASTING_ASSISTANT 
   2- CASTING_DIRECTOR
   3- EXECUTIVE_PRODUCER

Roles:
- Casting Assistant with permissions:
   - `get:movies-detail`
   - `get:actors`

- Casting Director with permissions:
   - `get:movies-detail`
   - `get:actors`
   - `post:actor`
   - `delete:actor`
   - `patch:actor`
   - `patch:movies`

- Executive Producer with permissions:
   - `get:movies-detail`
   - `get:actors`
   - `post:actor`
   - `delete:actor`
   - `patch:actor`
   - `patch:movies`
   - `post:movies`
   - `delete:movies`


      
Endpoints:
Get '/movies-detail'
 - get all movies in database:
 - sample result:
 "movies": {
        "1": "home alone",
        "2": "identity theft",
    }

POST '/movies'
 - to post new movie:

Patch '/movie/<id>'
 - params = <movie_id>
 - to edit movie data 

delete '/movies/<id>
 - params = <movie_id>
 - to delete specific movie

Get '/actors'
 - get all actors in database:
 - sample result:
   "actors": {
        "18": "Aisha",
        "19": "sama",
    }

POST '/actors'
 - to post new actors:

Patch '/actors/<id>'
 - params = <actor_id>
 - to edit actor data 

delete '/actors/<id>
 - params = <actor_id>
 - to delete specific actor

# Testing
 - to run the tests running:
   python test_app.py