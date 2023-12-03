from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Account.query.get(int(user_id))

class Account(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(320), unique=True, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(40), nullable=False)

    # Add a relationship to the 'post' table
    posts = db.relationship('Post', backref='author', lazy=True)

    # Add a relationship to the 'comment' table
    comments = db.relationship('Comment', backref='author', lazy=True)

    # Add a relationship to the 'destination_folder' table
    folders = db.relationship('DestinationFolder', backref='owner', lazy=True)

    # Add a relationship to the 'to_do_list' table
    to_do_lists = db.relationship('ToDoList', backref='owner', lazy=True)

    def get_id(self):
        return (self.user_id)

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    post_title = db.Column(db.String(20), nullable=False)
    post_content = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(40), nullable=False)
    images = db.Column(db.ARRAY(db.Text), nullable=False)
    post_date = db.Column(db.Date, nullable=False)
    tags = db.Column(db.ARRAY(db.Text), nullable=False, default=[])

    # Add a relationship to the 'comment' table
    comments = db.relationship('Comment', backref='post', lazy=True)

    # Add a relationship to the 'saved_destination' table
    saved_destinations = db.relationship('SavedDestination', backref='post', lazy=True)



class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    fk_post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    comment_content = db.Column(db.String(100), nullable=False)

class DestinationFolder(db.Model):
    folder_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    folder_name = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(255), nullable=False)

    # Add a relationship to the 'to_do_list' table
    to_do_lists = db.relationship('ToDoList', backref='folder', lazy=True)

    # Add a relationship to the 'saved_destination' table
    saved_destinations = db.relationship('SavedDestination', backref='folder', lazy=True)

class ToDoList(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    to_do_name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(100))
    due_date = db.Column(db.Date)
    # status BOOLEAN NOT NULL DEFAULT FALSE
    status = db.Column(db.Boolean, nullable=False, default=False)
    fk_folder_id = db.Column(db.Integer, db.ForeignKey('destination_folder.folder_id'))
    
    # saved_destinations = db.relationship('SavedDestination', backref='to_do_list', lazy=True)


class SavedDestination(db.Model):
    saved_destination_id = db.Column(db.Integer, primary_key=True)
    fk_folder_id = db.Column(db.Integer, db.ForeignKey('destination_folder.folder_id'), primary_key=True)
    fk_post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), primary_key=True)

    # to_do_list = db.relationship('ToDoList', backref='saved_destination_to_do_list', lazy=True)
    # post = db.relationship('Post', backref='saved_destination_post', lazy=True)
    # destination_folder = db.relationship('DestinationFolder', backref='saved_destination_folder', lazy=True)


