from ast import arguments
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request, jsonify

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt_identity

from db import db
from models.user import UserModel

from schemas import UserSchema


blp = Blueprint('Users', __name__, description="Operations on User")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email==user_data["email"]).first()
        print("==> USER : ",user)
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=user.id)
            return {"token":access_token}
        abort(401, message="invalid credentials !")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.email==user_data["email"]).first():
            abort(409, message = "A user with that username already exists.")
        user = UserModel(
            email=user_data["email"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return {"message":"User created succesfully"}, 201

@blp.route("/user/<int:user_id>")
class GetUser(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.filter(UserModel.id==user_id).first()
        if not user:
            abort(400, message = "User doesn't exist !")
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        if not user:
            abort(400, message="User doesn't exist !")
        db.session.delete(user)
        db.session.commit()
        return {"message":"user deleted !"},200

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        users = UserModel.query.filter()
        print("======>",users)
        return users

@blp.route("/verify")
class UserLogin(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(user_id=current_user), 200     
