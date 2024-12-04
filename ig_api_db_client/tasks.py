# tasks.py
from ig_api_db_client import create_app

app = create_app()
celery = app.celery  # Get the celery instance from the app

from ig_api_db_client.instagram_client import InstagramClient
from ig_api_db_client.models import User, SocialMediaAccount, Post, PostStat
from ig_api_db_client.database import db
import logging
from datetime import datetime

@celery.task
def fetch_user_data(username):
    try:
        # Access the Instagram client singleton
        cl = InstagramClient.get_instance().get_client()
        
        # Fetch user info
        user_info = cl.user_info_by_username(username)
        
        # Check if user exists in the database
        user = User.query.filter_by(username=username).first()
        if not user:
            # Create User instance
            user = User(
                username=username,
                email='',  # Placeholder, update as needed
                password_hash='',  # Placeholder, update as needed
            )
            db.session.add(user)
            db.session.commit()

        # Check if social media account exists
        account = SocialMediaAccount.query.filter_by(user_id=user.user_id, platform='instagram', username=username).first()
        if not account:
            account = SocialMediaAccount(
                user_id=user.user_id,
                platform='instagram',
                username=username,
            )
            db.session.add(account)
            db.session.commit()

        # Fetch user media
        medias = cl.user_medias(user_info.pk, amount=20)
        for media in medias:
            # Check if post already exists
            existing_post = Post.query.filter_by(external_id=str(media.pk), account_id=account.account_id).first()
            if existing_post:
                continue  # Skip if already exists

            post = Post(
                account_id=account.account_id,
                platform='instagram',
                external_id=str(media.pk),
                description=media.caption_text or '',
                media_url=media.thumbnail_url or media.video_url or '',
                media_type=media.media_type,
                likes=media.like_count,
                views=media.view_count,
                comments=media.comment_count,
                create_time=media.taken_at,
            )
            db.session.add(post)
            db.session.commit()

            # Optionally, add an initial PostStat record
            post_stat = PostStat(
                post_id=post.post_id,
                likes=post.likes,
                views=post.views,
                comments=post.comments,
            )
            db.session.add(post_stat)
            db.session.commit()
        
        logging.info(f"Successfully fetched and stored data for user: {username}")
        return f"Successfully fetched and stored data for user: {username}"
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error fetching data for user {username}: {e}")
        return f"Error fetching data for user {username}: {e}"

@celery.task
def fetch_hashtag_data(hashtag):
    try:
        # Access the Instagram client singleton
        cl = InstagramClient.get_instance().get_client()
        
        # Fetch top media for the hashtag
        medias = cl.hashtag_medias_top(hashtag, amount=20)
        
        for media in medias:
            # Fetch user info
            user_info = cl.user_info(media.user_id)
            username = user_info.username

            # Check if user exists in the database
            user = User.query.filter_by(username=username).first()
            if not user:
                user = User(
                    username=username,
                    email='',  # Placeholder, update as needed
                    password_hash='',  # Placeholder, update as needed
                )
                db.session.add(user)
                db.session.commit()

            # Check if social media account exists
            account = SocialMediaAccount.query.filter_by(user_id=user.user_id, platform='instagram', username=username).first()
            if not account:
                account = SocialMediaAccount(
                    user_id=user.user_id,
                    platform='instagram',
                    username=username,
                )
                db.session.add(account)
                db.session.commit()

            # Check if post already exists
            existing_post = Post.query.filter_by(external_id=str(media.pk), account_id=account.account_id).first()
            if existing_post:
                continue  # Skip if already exists

            post = Post(
                account_id=account.account_id,
                platform='instagram',
                external_id=str(media.pk),
                description=media.caption_text or '',
                media_url=media.thumbnail_url or media.video_url or '',
                media_type=media.media_type,
                likes=media.like_count,
                views=media.view_count,
                comments=media.comment_count,
                create_time=media.taken_at,
            )
            db.session.add(post)
            db.session.commit()

            # Optionally, add an initial PostStat record
            post_stat = PostStat(
                post_id=post.post_id,
                likes=post.likes,
                views=post.views,
                comments=post.comments,
            )
            db.session.add(post_stat)
            db.session.commit()
        
        logging.info(f"Successfully fetched and stored data for hashtag: #{hashtag}")
        return f"Successfully fetched and stored data for hashtag: #{hashtag}"
    
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error fetching data for hashtag #{hashtag}: {e}")
        return f"Error fetching data for hashtag #{hashtag}: {e}"
