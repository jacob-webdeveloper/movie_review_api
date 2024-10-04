from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from init import db
from models.review import Review, review_schema, reviews_schema
from models.movies import Movie

reviews_bp = Blueprint("reviews", __name__, url_prefix="/<int:movie_id>/reviews")


@reviews_bp.route("/", methods=["POST"])
@jwt_required()
def create_review(movie_id):
    body_data = request.get_json()
    stmt = db.select(Movie).filter_by(id=movie_id)
    movie = db.session.scalar(stmt)
    if movie:
        review = Review (
            review = body_data.get("review"),
            rating = body_data.get("rating"),
            movie = movie,
            user_id = get_jwt_identity()
        )
        db.session.add(review)
        db.session.commit()
        return review_schema.dump(review), 201
    else:
        return {"error": f"Movie with id {movie_id} not found."}, 404
    

@reviews_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(movie_id, review_id):
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        db.session.delete(review)
        db.session.commit()
        return {"message": f"Review '{review.review}' deleted successfully."}
    else:
        return {"error": f"Review with id {review_id} not found"}, 404



@reviews_bp.route("/<int:review_id>", methods=["PUT", "PATCH"])
@jwt_required()
def update_review(movie_id, review_id):
    body_data = request.get_json()
    stmt = db.select(Review).filter_by(id=review_id)
    review = db.session.scalar(stmt)
    if review:
        review.message = body_data.get("review") or review.message
        db.session.commit()
        return review_schema.dump(review)
    else:
        return {"error": f"review with id {review_id} not found."}, 404