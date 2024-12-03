from ig_api_db_client.database import db
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)  # SERIAL PRIMARY KEY
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    social_accounts = db.relationship('SocialMediaAccount', backref='user', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

class SocialMediaAccount(db.Model):
    __tablename__ = 'social_media_accounts'

    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    platform = db.Column(db.Enum('instagram', 'tiktok', name='platform_enum'), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    api_key = db.Column(db.String(255))
    two_fa_secret = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship('Post', backref='social_account', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'account_id': self.account_id,
            'user_id': self.user_id,
            'platform': self.platform,
            'username': self.username,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('social_media_accounts.account_id', ondelete='CASCADE'), nullable=False)
    platform = db.Column(db.Enum('instagram', 'tiktok', name='platform_enum'), nullable=False)
    external_id = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    media_url = db.Column(db.String(255))
    media_type = db.Column(db.String(20))
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime)
    stored_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Unique constraint on (external_id, account_id)
    __table_args__ = (db.UniqueConstraint('external_id', 'account_id', name='_external_account_uc'),)

    def to_dict(self):
        return {
            'post_id': self.post_id,
            'account_id': self.account_id,
            'platform': self.platform,
            'external_id': self.external_id,
            'description': self.description,
            'media_url': self.media_url,
            'media_type': self.media_type,
            'likes': self.likes,
            'views': self.views,
            'shares': self.shares,
            'comments': self.comments,
            'create_time': self.create_time.isoformat() if self.create_time else None,
            'stored_time': self.stored_time.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

class PostStat(db.Model):
    __tablename__ = 'post_stats'

    stat_id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id', ondelete='CASCADE'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    views = db.Column(db.Integer, default=0)
    shares = db.Column(db.Integer, default=0)
    comments = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'stat_id': self.stat_id,
            'post_id': self.post_id,
            'timestamp': self.timestamp.isoformat(),
            'likes': self.likes,
            'views': self.views,
            'shares': self.shares,
            'comments': self.comments,
        }
