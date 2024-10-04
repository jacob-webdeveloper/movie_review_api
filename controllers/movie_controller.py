from flask import Blueprint, request
from init import db
from models.movies import Movie, movie_schema, movies_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

movies_bp = Blueprint("movies", __name__, url_prefix="/movies")

@movies_bp.route("/")
def get_all_movies():
    stmt = db.select(Movie)
    movies = db.session.scalars(stmt)
    if movies:
        return movies_schema.dump(movies)
    else:   
        return {"error": "No Movies were found"}, 404
        


@movies_bp.route("/<int:movie_id>")
def get_a_movie(movie_id):
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        return movie_schema.dump(movie)
    else:   
        return {"error": f"Movie with id {movie_id} not found"}, 404
    

@movies_bp.route("/", methods=["POST"])
@jwt_required()
def create_movie():
    body_data = request.get_json()
    movie = Movie(
        movie_title = body_data.get("movie_title"),
        release_year = body_data.get("release_year"),
        user_id = get_jwt_identity()
    )
    db.session.add(movie)
    db.session.commit()
    return movie_schema.dump(movie)


@movies_bp.route("/<int:movie_id>", methods=["DELETE"])
@jwt_required()
def delete_movie(movie_id):
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        db.session.delete(movie)
        db.session.commit()
        return {"message": f"Movie {movie.movie_title} deleted successfully!"}
    else:
        return {"error": f"Movie with id {movie_id} not found"}, 404
    

@movies_bp.route("/<int:movie_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_movie(movie_id):
    body_data = request.get_json()
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie: 
        movie.movie_title = body_data.get("movie_title") or movie.movie_title
        movie.release_year = body_data.get("release_year") or movie.release_year

        db.session.commit()
        return movie_schema.dump(movie)
    else:   
        return {"error": f"Movie with id {movie_id} not found."}, 404
        