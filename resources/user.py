from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from schema import UserSchema
from models import UserModel


blp = Blueprint("Users", __name__, description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first():
            abort(409, message="A user with the given username already exists.")
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/register-admin")
class AdminRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, admin_data):
        if UserModel.query.filter(
            UserModel.username == admin_data["username"]
        ).first():
            abort(409, message="A user with the given username already exists.")
        
        admin = UserModel(username=admin_data["username"],
            password=pbkdf2_sha256.hash(admin_data["password"]), 
            is_admin=True)

        db.session.add(admin)
        db.session.commit()
        return admin


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=str(user.user_id))
            return {"access_token": access_token}, 200
        
        abort(401, message="Invalid credentials.")


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    admin and testing only
    """
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        if get_jwt().get("is_admin"):
            user = UserModel.query.get_or_404(user_id)
            return user
        abort(401, message="Admin privilege required.")
    
    @jwt_required()
    def delete(self, user_id):
        if get_jwt().get("is_admin"):
            user = UserModel.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted."}, 200
        abort(401, message="Admin privilege required.")