import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actor, Movie
from auth import requires_auth, AuthError

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        selections = Actor.query.all()
        if selections is None:
            abort(404)
        
        actors = [actor.format() for actor in selections]

        return jsonify({
            'success': True,
            'actors': actors
        })
    
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        
        try:
            actor.delete()
            return jsonify({
                'success': True,
                'actor_id': actor_id
            })
        except:
            abort(422)
    
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(jwt):
        body = request.get_json()
        if body is None:
            abort(422)
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if name is None or age is None or gender is None:
            abort(422)
        
        try:
            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
            return jsonify({
                'success': True,
                'actors': actor.format()
            })
        except:
            abort(422)
    
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        actor = Actor.query.get(actor_id)
        body = request.get_json()
        if body is None:
            abort(422)
        name = body.get('name')
        age = body.get('age')
        gender = body.get('gender')

        if actor is None:
            abort(404)
        if name is None and age is None and gender is None:
            abort(422)
        
        try:
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            actor.update()

            return jsonify({
                'success': True,
                'actors': actor.format()
            })
        except:
            abort(422)
    

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        selections = Movie.query.all()
        if selections is None:
            abort(404)
        
        movies = [movie.format() for movie in selections]

        return jsonify({
            'success': True,
            'movies': movies
        }) 
    
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        
        try:
            movie.delete()
            return jsonify({
                'success': True,
                'movie_id': movie_id
            })
        except:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(jwt):
        body = request.get_json()
        if body is None:
            abort(422)
        title = body.get('title')
        release_date = body.get('release_date')
        print(title, release_date)

        if title is None or release_date is None:
            abort(422)
        
        try:
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify({
                'success': True,
                'movies': movie.format()
            })
        except:
            abort(422)

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        movie = Movie.query.get(movie_id)
        body = request.get_json()
        if body is None:
            abort(422)
        title = body.get('title')
        release_date = body.get('release_date')

        if movie is None:
            abort(404)
        if title is None and release_date is None:
            abort(422)
        
        try:
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            movie.update()

            return jsonify({
                'success': True,
                'movies': movie.format()
            })
        except:
            abort(422)

#----------------------------------------------------------------------------#
# Error Handllers.
#----------------------------------------------------------------------------#

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found.'
        }), 404
    
    @app.errorhandler(422)
    def not_found_error(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Request was unprocessable.'
        }), 422
    
    @app.errorhandler(AuthError)
    def auth_error(ex):
        return jsonify({
            'success': False,
            'error': ex.status_code,
            'message': ex.error['description']
        }), ex.status_code
    
    

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)