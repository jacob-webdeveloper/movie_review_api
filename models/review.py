from init import db, ma
from marshmallow import fields

class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"), nullable=False)

    user = db.relationship("User", back_populates="reviews")
    movie = db.relationship("Movie", back_populates="reviews")

class ReviewSchema(ma.Schema):
    user = fields.Nested("UserSchema", only=["name", "email"])
    movie = fields.Nested("MovieSchema", exclude=["reviews"])
    class Meta:
        fields = ("id", "message", "date", "user", "movie")
    
review_schema = ReviewSchema()
reviews_schema = ReviewSchema(many=True)

