from flask import Blueprint, request, jsonify
from ig_api_db_client.models import User, SocialMediaAccount, Post
from ig_api_db_client.tasks import fetch_user_data, fetch_hashtag_data
from ig_api_db_client.database import db

api = Blueprint('api', __name__)

@api.route('/user/<username>', methods=['GET'])
def get_user(username):
    # Check if user data exists in the database
    user = User.query.filter_by(username=username).first()
    if user:
        # Fetch associated social media accounts and posts
        accounts = SocialMediaAccount.query.filter_by(user_id=user.user_id).all()
        user_data = user.to_dict()
        user_data['social_accounts'] = [account.to_dict() for account in accounts]
        return jsonify({'user': user_data}), 200
    else:
        # Start background task to fetch data
        task = fetch_user_data.delay(username)
        return jsonify({'status': 'processing', 'task_id': task.id}), 202

@api.route('/hashtag/<hashtag>', methods=['GET'])
def get_hashtag(hashtag):
    # Start background task to fetch hashtag data
    task = fetch_hashtag_data.delay(hashtag)
    return jsonify({'status': 'processing', 'task_id': task.id}), 202

@api.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    from celery.result import AsyncResult
    result = AsyncResult(task_id)
    if result.state == 'PENDING':
        response = {
            'state': result.state,
            'status': 'Pending...'
        }
    elif result.state != 'FAILURE':
        response = {
            'state': result.state,
            'result': result.result
        }
        if result.state == 'SUCCESS':
            response['result'] = result.result
    else:
        response = {
            'state': result.state,
            'status': str(result.info),
        }
    return jsonify(response)
