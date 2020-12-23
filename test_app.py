
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from app import create_app
from models import *

load_dotenv()

class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.assistant = os.getenv('casting_assistant_jwt')
        self.director = os.getenv('casting_director_jwt')
        self.producer = os.getenv('executive_producer_jwt')
        setup_db(self.app)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    #get movies - error behavior 
    #When there is no movies
    def test_movies_failure_scenario(self):
        response = self.client().get('/movies-detail', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.assistant)
                                })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    #post movie - success behavior
    def test_post_movie(self):
        post_movie = {
            "title": "home alone",
            "release_date": "1992-02-02",
            "genre": "comedy"
        }
        response = self.client().post('/movies',headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer)
                                }, json=post_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    
    #get movies - success behavior
    def test_movies(self):
        response = self.client().get('/movies-detail', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.assistant)
                                })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
    


    # post movies - error behavior
    def test_post_movie_error_422(self):
        post_movie = {
            "title": "home alone",
            "release_date": "1992-02-02"
        }
        response = self.client().post('/movies',headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer)
                                }, json=post_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)

    #patch movie  - success behavior
    def test_patch_movie(self):
        patch_movie = {
            "release_date": "1993-02-02"
        }
        response = self.client().patch('/movies/5', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director)
                                }, json=patch_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    #patch movie - error behavior
    def test_patch_movie_error_404(self):
        patch_movie = {
            "release_date": "1993-02-02"
        }
        response = self.client().patch('/movies/333', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer)
                                }, json=patch_movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    #delete movie - success behavior
    def test_delete_movie(self):
        res = self.client().delete('/movies/8', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer )
                                } )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    #delete movie - error behavior
    def test_delete_movie_error_404(self):
        res = self.client().delete('/movies/222', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer )
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)



    #get actors - error behavior
    #When there is no actors
    def test_actors_failure_scenario(self):
        response = self.client().get('/actors',headers={
                                    "Authorization": "Bearer {}".format(
                                        self.assistant )
                                } )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


    #post actor - success behavior
    def test_post_actor(self):
        post_actor = {
            "name": "Aisha",
            "age": "22",
            "gender": "female"
        }
        response = self.client().post('/actors',headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director )
                                }, json=post_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    #get actors - success behavior
    def test_actors(self):
        response = self.client().get('/actors', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director )
                                })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    

    #post actor - error behavior
    def test_post_actor_error_422(self):
        post_actor = {
            "name": "Aisha",
            "age": "22"
        }
        response = self.client().post('/movies', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director )
                                }, json=post_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)


    #patch actor - success behavior
    def test_patch_actor(self):
        patch_actor = {
            "age": "23"
        }
        response = self.client().patch('/actors/18', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer )
                                },json=patch_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    #patch actor - error behavior
    def test_patch_actor_error_404(self):
        patch_actor = {
            "age": "23"
        }
        response = self.client().patch('/actors/555', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director )
                                },json=patch_actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    # delete actor - success behavior
    def test_delete_actor(self):
        res = self.client().delete('/actors/21', headers={
                                    "Authorization": "Bearer {}".format(
                                        self.director )
                                },)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # delete actor - error behavior
    def test_delete_actor_error_404(self):
        res = self.client().delete('/actors/222',headers={
                                    "Authorization": "Bearer {}".format(
                                        self.producer )
                                },)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)


if __name__ == "__main__":
    unittest.main()