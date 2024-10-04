from init import db, ma
from marshmallow import fields

class Movie(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # genre_id = db.Column(db.String, db.ForeignKey("genre.id"), nullable=False)
    # director_id = db.Column(db.String, db.ForeignKey("director.id"), nullable=False)

    user = db.relationship('User', back_populates='movies')


class MovieSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["id", "name", "email"])

    class Meta:
        fields = ("id", "movie_title", "release_year", "user")#"genre_id", "director_id")

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

