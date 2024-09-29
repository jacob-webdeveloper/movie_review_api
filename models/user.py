from init import db, ma

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)


class UserSchema(ma.Schema)
    class Meta:
        fields = ("id", "name", "email", "password")

# To handle a single user object
user_schema = UserSchema(exclude=["password"])

# To handle a list of user objects
user_schema = UserSchema(many=True, exclude=["password"])