import uuid
from flask import request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
import redis
from pymodm.errors import DoesNotExist
from  werkzeug.security import generate_password_hash, check_password_hash

import config
from models import User


# jwt_redis_blocklist = redis.StrictRedis(
#     host="localhost", port=6379, db=0, decode_responses=True
# )

# @jwt.token_in_blocklist_loader
# def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
#     jti = jwt_payload["jti"]
#     token_in_redis = jwt_redis_blocklist.get(jti)
#     return token_in_redis is not None


def login():
    # creates dictionary of form data
    auth = request.json

    email = auth.get("email")
    password = auth.get("password")
    
    # validating the inputs
    if not auth or not email or not password:
        # returns 401 if any email or / and password is missing
        return jsonify(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )

    try:
        user = User.objects.get_by_email(email).first()
    except DoesNotExist:
        user = None

    if not user:
        # returns 401 if user does not exist
        return jsonify(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({'access_token' : access_token, 'refresh_token': refresh_token}), 201
    # returns 403 if password is wrong
    return jsonify(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )

@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)

def signup():
    # creates a dictionary of the form data
    data = request.json

    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    try:
        user = User.objects.get_by_email(email).first()
    except DoesNotExist:
        user = None
    if not user:
        user = User(
            id = str(uuid.uuid4()),
            name = name,
            email = email,
            password = generate_password_hash(password)
        ).save()
        return jsonify({'message' :'Successfully registered.'}), 201

    return jsonify({'message' :'User already exists. Please Log in.'}), 202

@jwt_required()
def logout():
    # jti = get_jwt()["jti"]
    # jwt_redis_blocklist.set(jti, "", ex=config.ACCESS_EXPIRES)
    # return jsonify(msg="Access token revoked"), 401
    pass