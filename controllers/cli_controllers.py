from flask import Blueprint
from init import db, bcrypt
from models.user import User
from models.movies import Movie
from models.review import Review


db_commands = Blueprint("db", __name__)

@db_commands.cli.command("create")
def create_tables():
    db.create_all()
    print("Tables created!")

@db_commands.cli.command("seed")
def seed_tables():
    users = [
        User(
            email = "admin@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8"),
        ), 
        User(
            name = "User A",
            email = "usera@email.com",
            password = bcrypt.generate_password_hash("123456").decode("utf-8")
        )
    ]

    db.session.add_all(users)

    movies = [
        Movie(
            movie_title = "Movie 1",
            release_year = "2024",
            user = users[0]
            # genre_id = genre[0]
            # directory_id = director[0]
        ), 
        Movie(
            movie_title = "Movie 2",
            release_year = "2022",
            user = users[0]
            # genre_id = genre[0]
            # directory_id = director[0]
        ), 
        Movie(
            movie_title = "Movie 3",
            release_year = "1990",
            user = users[1]
            # genre_id = genre[0]
            # directory_id = director[0]
        )]
        
    
    db.session.add_all(movies)

    db.session.commit()

    print("Tables seeded!")

@db_commands.cli.command("drop")
def drop_tables():
    db.drop_all()
    print("Tables dropped.")