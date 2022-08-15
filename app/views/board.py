from datetime import timedelta
import uuid
import redis
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request, jsonify
from functools import wraps

from ..util import get_user
from ..models import Board
from .. import config

redis_client = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)

def rate_limit(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = f"{get_jwt_identity()}:{request.path}"
        requests_count = redis_client.get(key)
        if requests_count is None:
            redis_client.set(key, 1, ex=timedelta(minutes=1))
        if requests_count > config.RATE_LIMIT:
            return jsonify({"message": "Too many requests"}), 429
        redis_client.incr(key)
        return f(*args, **kwargs)
    return decorated_function

@jwt_required()
@rate_limit
def create_board():
    data = request.json

    title, description = data.get("title"), data.get("description")

    user_id = get_jwt_identity()

    user = get_user(user_id)
    if user is None:
        return jsonify({"message" : "please login first"}), 401

    try:
        board = Board(str(uuid.uuid4()), title, description, user).save()
    except Exception as e:
        print("error in creating new board", e)
        return jsonify({'message' : 'creating new board failed.'}), 400

    return jsonify({
        'message' : 'Board created successfully.',
        'board' : board.id
    }), 201


@jwt_required()
def get_board(id):
    try:
        board = Board.objects.raw({'_id': id}).first()
    except:
        return jsonify({'message' : 'Board does not exist.'}), 404
    
    return jsonify({
        "title": board.title,
        "description": board.description,
    }), 200


@jwt_required()
def get_user_boards():
    user_id = get_jwt_identity()
    user_boards = Board.objects.raw({'user': user_id}).all()
    boards = [{"title": b.title, "description": b.description} for b in user_boards]
    return jsonify({ "message": "success", "boards": boards }), 200


@jwt_required
def update_board(id):
    user_id = get_jwt_identity()
    data = request.json

    title = data.get("title", None)
    description = data.get("description", None)

    try:
        board = Board.objects.raw({'_id': id}).first()
    except:
        return jsonify({'message' : 'Board does not exist.'}), 404

    # checking permission
    if board.user.id != user_id:
        return jsonify({'message' : 'You are not authorized to update this board.'}), 401
    
    board.title = title
    board.description = description

    try:
        board.save()
    except:
        return jsonify({'message' : 'Updating board failed.'}), 400
    
    return jsonify({'message': 'Board updated successfully.'}), 200
    

