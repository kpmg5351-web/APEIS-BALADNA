from backend.database import db, TimestampMixin, UUIDMixin

class Post(UUIDMixin, TimestampMixin, db.Model):
    """Social feed posts - مشاركات المستخدمين"""
    __tablename__ = 'posts'
    
    # Content
    text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))  # أخبار واستفسارات, خدمات ومساعدة, مفقودات ومثبتات, فعاليات ومناسبات
    
    # Author & Village
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    village_id = db.Column(db.String(36), db.ForeignKey('villages.id'), nullable=True, index=True)
    
    # Visibility
    is_published = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Stats
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    views_count = db.Column(db.Integer, default=0)
    
    # Relationships
    comments = db.relationship('Comment', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.id[:8]} by {self.author.name}>'
    
    def to_dict(self, include_comments=False):
        data = {
            'id': self.id,
            'text': self.text,
            'category': self.category,
            'author': self.author.to_dict(),
            'village_id': self.village_id,
            'village_name': self.village.name if self.village else None,
            'likes_count': self.likes_count,
            'comments_count': self.comments_count,
            'views_count': self.views_count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        if include_comments:
            data['comments'] = [c.to_dict() for c in self.comments.all()]
        return data


class Comment(UUIDMixin, TimestampMixin, db.Model):
    """Comments on posts"""
    __tablename__ = 'comments'
    
    # Content
    text = db.Column(db.Text, nullable=False)
    
    # Relations
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=False, index=True)
    author_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Status
    is_deleted = db.Column(db.Boolean, default=False)
    likes_count = db.Column(db.Integer, default=0)
    
    def __repr__(self):
        return f'<Comment {self.id[:8]} by {self.author.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'author': self.author.to_dict(),
            'post_id': self.post_id,
            'likes_count': self.likes_count,
            'created_at': self.created_at.isoformat(),
        }


class Like(UUIDMixin, TimestampMixin, db.Model):
    """Likes on posts and comments"""
    __tablename__ = 'likes'
    
    # Relations
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False, index=True)
    post_id = db.Column(db.String(36), db.ForeignKey('posts.id'), nullable=True, index=True)
    comment_id = db.Column(db.String(36), db.ForeignKey('comments.id'), nullable=True, index=True)
    
    # Constraint: must like either post or comment, not both
    __table_args__ = (
        db.CheckConstraint('(post_id IS NOT NULL AND comment_id IS NULL) OR (post_id IS NULL AND comment_id IS NOT NULL)'),
    )
    
    def __repr__(self):
        return f'<Like by {self.user.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'post_id': self.post_id,
            'comment_id': self.comment_id,
            'created_at': self.created_at.isoformat(),
        }
