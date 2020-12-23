#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask,abort, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from models import *
import datetime
from auth.auth import AuthError, requires_auth
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')

        return response
  
  #Endpoints

  # 1-Movies

    @app.route('/')
    def hello():
        return jsonify({'message': 'HELLO WORLD'})

        
    @app.route('/movies-detail', methods=['GET'], endpoint='movies_detail')
    @requires_auth('get:movies-detail')
    def movies_detail(jwt):
        movies = Movie.query.all()
        if len(movies) == 0:
            abort(404)
        allmovies = {}
        for movie in movies:
            allmovies[movie.id] = movie.title

        return jsonify({
          'success': True,
          'movies': allmovies
        })


    @app.route('/movies', methods=['POST'], endpoint='post_movie')
    @requires_auth('post:movies')
    def movies(jwt):
        try:
            data = request.get_json()
            movie = Movie(title=data['title'],
                          release_date=datetime.date.fromisoformat(data['release_date']),
                          genre=data['genre'])
            
            movie.insert()
            return jsonify({
                'success': True
                }), 200
        except:
            abort(422)

    
    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def movies(jwt, id):
        try:
            data = request.get_json()
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie:
                if 'title' in data:
                    movie.title = data['title']
                if 'release_date' in data:
                    movie.release_date = data['release_date']
                if 'genre' in data:
                    movie.genre = data['genre']
                movie.update()
                return jsonify({
                    'success': True, 
                    }), 200
            else:
                return jsonify({
                    'success': False,
                }), 404
        except:
            return jsonify({
                'success': False,
                'error': "An error occurred"
            }), 500
    
    @app.route('/movies/<id>', methods=['DELETE'], endpoint='delete_movie')
    @requires_auth('delete:movies')
    def movies(jwt, id):
        try:
            movie = movie = Movie.query.filter(Movie.id == id).one_or_none()
            if movie:
                movie.delete()
                return jsonify({'success': True, 'movie': id}), 200
            else:
                return jsonify({
                    'success':False,
                    'error':
                    'Movie #' + id + ' not found to be deleted'
                }), 404
        except:
            return jsonify({
                'success': False,
                'error': "An error occurred"
            }), 500
    
    
    
      # 2-Actor:
    @app.route('/actors', methods=['GET'], endpoint='get-actors')
    @requires_auth('get:actors')
    def actors(jwt):
        actors = Actor.query.all()
        if len(actors) == 0:
            abort(404)
        allactors = {}
        for actor in actors:
            allactors[actor.id] = actor.name

        return jsonify({
          'success': True,
          'actors': allactors
        })
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def actors(jwt):
        try:
            data = request.get_json()
            actor = Actor(name=data['name'],
                          age=data['age'],
                          gender=data['gender'])
            
            actor.insert()
            return jsonify({
                'success': True
            }), 200
        except:
            abort(422)
    
    @app.route('/actors/<id>', methods=['PATCH'], endpoint='patch_actor')
    @requires_auth('patch:actor')
    def actors(jwt, id):
        try:
            data = request.get_json()
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor:
                if 'name' in data:
                    actor.name = data['name']
                if 'gender' in data:
                    actor.gender = data['gender']
                if 'age' in data:
                    actor.age = data['age']
                actor.update()
                return jsonify({
                    'success': True, 
                    # 'actors': [actor.long()]
                    }), 200
            else:
                return jsonify({
                    'success': False,
                    'error':
                    'Actor #' + id + ' not found to be edited'
                }), 404
        except:
            return jsonify({
                'success': False,
                'error': "An error occurred"
            }), 500
    
    
    @app.route('/actors/<id>', methods=['DELETE'], endpoint='delete_actor')
    @requires_auth('delete:actor')
    def actors(jwt, id):
        try:
            actor = actor = Actor.query.filter(Actor.id == id).one_or_none()
            if actor:
                actor.delete()
                return jsonify({'success': True, 'actor': id}), 200
            else:
                return jsonify({
                    'success':False,
                    'error':
                    'Actor #' + id + ' not found to be deleted'
                }), 404
        except:
            return jsonify({
                'success': False,
                'error': "An error occurred"
            }), 500

    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "server error"
        }), 500
    

    return app

app = create_app()