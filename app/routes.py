# ChatGPT Generated Structure
# TODO: Please verify that the function stubs are correct
# Note: The functions are yet to be implemented!

from app.models import Account, Post, Comment, DestinationFolder, ToDoList, SavedDestination

from flask import Flask, request, jsonify
from app import app, db, bcrypt

# User Account Routes
@app.route('/api/account/new', methods=['POST'])
def create_account():
    data = request.get_json()

    print(data)
    output = "Failure!"
    # check if the email is already in use
    if not Account.query.filter_by(email=data['email']).first():
        

        acc = Account(  email = data['email'],
                    name = data['name'],
                    location = data['location'])
   
        db.session.add(acc)
        db.session.commit()

        output = "Success!"

    return jsonify({"message": output})

@app.route('/api/account/<int:user_id>', methods=['GET'])
def get_account(user_id):
    acc = Account.query.filter_by(user_id=user_id).first()

    account = {
        "email": acc.email,
        "name": acc.name,
        "location": acc.location
    }

    return jsonify(account)

@app.route('/api/account/update/<int:user_id>', methods=['PUT'])
def update_account(user_id):
    data = request.get_json()

    acc = Account.query.filter_by(user_id=user_id).first()
    acc.email = data['email']
    acc.name = data['name']
    acc.location = data['location']

    db.session.commit()

    return jsonify({"message": "Account updated!"})

@app.route('/api/account/delete/<int:user_id>', methods=['DELETE'])
def delete_account(user_id):
    acc = Account.query.filter_by(user_id=user_id).first()

    db.session.delete(acc)
    db.session.commit()

    return jsonify({"message": "Account deleted!"})

@app.route('/api/account/check/<string:email>', methods=['GET'])
def check_account(email):
    acc = Account.query.filter_by(email=email).first()

    if acc:
        return jsonify({"message": "Account exists!"})
    else:
        return jsonify({"message": "Account does not exist!"})
    
# Post Routes
@app.route('/api/post/create/<int:user_id>', methods=['POST'])
def create_post(user_id):
   
    print("Creating a post")
    data = request.get_json()

    # data looks like
    """{
    "title": "My First Post", 
    "author": 4352
    "date": "2021-04-01",
    "location": "Leh, Ladakh",
    "tags": ["travel", "food", "adventure"],
    "image_uids": ["https://example.com/1", "https://example.com/2", "https://example.com/3"],
    "description": "This is my first post!", 
    }"""

    # post_id integer NOT NULL GENERATED ALWAYS AS IDENTITY (INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1),
    # fk_user_id integer NOT NULL,
    # post_title character varying(20) COLLATE pg_catalog."default" NOT NULL,
    # post_content character varying(256) COLLATE pg_catalog."default" NOT NULL,
    # location character varying(40) COLLATE pg_catalog."default" NOT NULL,
    # images text[] COLLATE pg_catalog."default" NOT NULL,
    # tags text[] COLLATE pg_catalog."default" NOT NULL DEFAULT '{}';
    # post_date date NOT NULL,
    
    print(data)

    print("Description: ", data['description'])
    # create a post object
    
    post = Post( fk_user_id = data['author'],
                 post_title = data['title'],
                 post_content = data['description'],
                 location = data['location'],
                 images = data['image_uids'],
                 post_date = data['date'],
                 tags = data['tags']
                 )
    
    db.session.add(post)
    db.session.commit()


    
    return jsonify(data)


@app.route('/api/post/all', methods=['GET'])
def get_all_posts():
    
    print("Getting all posts")

    # get all posts
    filttered_posts = Post.query.all()

    print("All posts fetched")

    # create a list of posts
    posts = []

    # posts should be a list of
    """{
    "title": "My First Post", 
    "author": 4352
    "date": "2021-04-01",
    "location": "Leh, Ladakh",
    "tags": ["travel", "food", "adventure"],
    "image_uids": ["https://example.com/1", "https://example.com/2", "https://example.com/3"],
    "description": "This is my first post!", 
    }"""

    # date format: 2021-04-01 and Time zone: EST
    for post in filttered_posts:
        formatted_date = post.post_date.strftime("%Y-%m-%d")

        posts.append({"title": post.post_title,
                      "author": post.fk_user_id,
                      "date": formatted_date,
                      "location": post.location,
                      "tags": post.tags,
                      "image_uids": post.images,
                      "description": post.post_content
                      })
    print(posts)
    return jsonify(posts)
    return jsonify({"message": "All posts fetched!"})


@app.route('/api/post/all/<int:user_id>', methods=['GET'])
def get_all_posts_by_user(user_id):
     
    # get all posts
    filttered_posts = Post.query.filter_by(fk_user_id=user_id).all()

    # create a list of posts
    posts = []

    # posts should be a list of
    """{
    "title": "My First Post", 
    "author": 4352
    "date": "2021-04-01",
    "location": "Leh, Ladakh",
    "tags": ["travel", "food", "adventure"],
    "image_uids": ["https://example.com/1", "https://example.com/2", "https://example.com/3"],
    "description": "This is my first post!", 
    }"""

    for post in filttered_posts:
        posts.append({"title": post.post_title,
                      "author": post.fk_user_id,
                      "date": post.post_date,
                      "location": post.location,
                      "tags": post.tags,
                      "image_uids": post.images,
                      "description": post.post_content
                      })
        
    return jsonify(posts)

# Not Done
@app.route('/api/post/from_collection/<int:collection_id>', methods=['GET'])
def get_all_posts_in_collection(collection_id):
    # collections is also called DestinationFolder
    saved_destinations = SavedDestination.query.filter_by(fk_folder_id=collection_id).all()

    # Create a list of posts
    posts = []

    # Iterate through saved_destinations and fetch the associated posts
    for saved_destination in saved_destinations:
        post = saved_destination.post
        posts.append({
            "title": post.post_title,
            "author": post.fk_user_id,
            "date": post.post_date,
            "location": post.location,
            "tags": post.tags,
            "image_uids": post.images,
            "description": post.post_content
        })

    return jsonify(posts)


@app.route('/api/post/<int:post_id>', methods=['GET'])
def get_post(post_id):

    # get the post
    post = Post.query.filter_by(post_id=post_id).first()

    # create a post object
    post = {"title": post.post_title,
            "author": post.fk_user_id,
            "date": post.post_date,
            "location": post.location,
            "tags": post.tags,
            "image_uids": post.images,
            "description": post.post_content
            }

    return jsonify(post)


@app.route('/api/post/update/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    data = request.get_json()

    
    post = Post.query.filter_by(post_id=post_id).first()
    post.post_title = data['title']
    post.post_content = data['description']
    post.location = data['location']
    post.images = data['image_uids']
    post.post_date = data['date']
    post.tags = data['tags']

    db.session.commit()

    return jsonify({"message": "Post updated!"})


@app.route('/api/post/delete/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
        
        # delete all comments associated with the post
        comments = Comment.query.filter_by(fk_post_id=post_id).all()
        for comment in comments:
            db.session.delete(comment)
            db.session.commit()
        
        # delete all saved destinations associated with the post
        saved_destinations = SavedDestination.query.filter_by(fk_post_id=post_id).all()
        for saved_destination in saved_destinations:
            db.session.delete(saved_destination)
            db.session.commit()

        post = Post.query.filter_by(post_id=post_id).first()
    
        db.session.delete(post)
        db.session.commit()
    
        return jsonify({"message": "Post deleted!"})


@app.route('/api/post/add_to_collection/<int:post_id>/<int:collection_id>', methods=['POST'])
def add_post_to_collection(post_id, collection_id):
        
    
    # add entry to the SavedDestination table
    saved_destination = SavedDestination( fk_post_id = post_id,
                                             fk_folder_id = collection_id)
    
    db.session.add(saved_destination)
    db.session.commit()

    return jsonify({"message": "Post added to collection!"})

@app.route('/api/post/remove_from_collection/<int:post_id>/<int:collection_id>', methods=['DELETE'])
def remove_post_from_collection(post_id, collection_id):
        
    # get the entry from the SavedDestination table
    saved_destination = SavedDestination.query.filter_by(fk_post_id=post_id, fk_folder_id=collection_id).first()

    db.session.delete(saved_destination)
    db.session.commit()

    return jsonify({"message": "Post removed from collection!"})


# Comment Routes


@app.route('/api/comment/create/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    # comment_id = db.Column(db.Integer, primary_key=True)
    # fk_user_id = db.Column(db.Integer, db.ForeignKey('account.user_id'), nullable=False)
    # fk_post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    # comment_content = db.Column(db.String(100), nullable=False)

    comment = Comment( fk_user_id = data['author'],
                          fk_post_id = post_id,
                          comment_content = data['content'])
    
    db.session.add(comment)
    db.session.commit()

    return jsonify({"message": "Comment created!"})


@app.route('/api/comment/all/<int:post_id>', methods=['GET'])
def get_all_comments(post_id):

    filtered_comments = Comment.query.filter_by(fk_post_id=post_id).all()

    comments = []

    for comment in filtered_comments:
        comments.append({"author": comment.fk_user_id,
                         "content": comment.comment_content
                         })
        
    return jsonify(comments)



@app.route('/api/comment/<int:comment_id>', methods=['GET'])
def get_comment(comment_id):
    
    comment = Comment.query.filter_by(comment_id=comment_id).first()

    comment = {"author": comment.fk_user_id,
            "content": comment.comment_content
            }

    return jsonify(comment)


@app.route('/api/comment/update/<int:comment_id>', methods=['PUT'])
def update_comment(comment_id):
    data = request.get_json()

    comment = Comment.query.filter_by(comment_id=comment_id).first()

    comment.comment_content = data['content']
    
    db.session.commit()

    return jsonify({"message": "Comment updated!"})


@app.route('/api/comment/delete/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):

    comment = Comment.query.filter_by(comment_id=comment_id).first()

    db.session.delete(comment)
    db.session.commit()

    return jsonify({"message": "Comment deleted!"})

# Collection Routes


@app.route('/api/collection/create/<int:user_id>', methods=['POST'])
def create_collection(user_id):
    data = request.get_json()
    
    folder = DestinationFolder( fk_user_id = user_id,
                                folder_name = data['name'],
                                location = data['location'])
    
    db.session.add(folder)
    db.session.commit()

    return jsonify({"message": "Collection created!"})
    

@app.route('/api/collection/all/<int:user_id>', methods=['GET'])
def get_all_collections(user_id):
    
    filtered_folders = DestinationFolder.query.filter_by(fk_user_id=user_id).all()

    folders = []

    for folder in filtered_folders:
        folders.append({"name": folder.folder_name,
                        "location": folder.location,
                        "id": folder.folder_id,
                        })
        
    return jsonify(folders)


@app.route('/api/collection/<int:collection_id>', methods=['GET'])
def get_collection(collection_id):
    
    folder = DestinationFolder.query.filter_by(folder_id=collection_id).first()

    folder = {"name": folder.folder_name,
              "location": folder.location
              }

    return jsonify(folder)


@app.route('/api/collection/update/<int:collection_id>', methods=['PUT'])
def update_collection(collection_id):
    data = request.get_json()
    
    folder = DestinationFolder.query.filter_by(folder_id=collection_id).first()

    folder.folder_name = data['name']
    folder.location = data['location']

    db.session.commit()

    return jsonify({"message": "Collection updated!"})


@app.route('/api/collection/delete/<int:collection_id>', methods=['DELETE'])
def delete_collection(collection_id):
    
    folder = DestinationFolder.query.filter_by(folder_id=collection_id).first()

    db.session.delete(folder)
    db.session.commit()

    return jsonify({"message": "Collection deleted!"})

# Task Routes
@app.route('/api/task/create', methods=['POST'])
def create_task():

    print("Creating a task")
    data = request.get_json()
    
    print(data)
    task = ToDoList( fk_user_id = data['author'],
                     to_do_name = data['name'],
                     description = data['description'],
                     due_date = data['date'],
                     fk_folder_id = data['collection_id'],
                     status = data['status'])
     
    db.session.add(task)
    db.session.commit()

    return jsonify({"message": "Task created!"})

@app.route('/api/task/all/<int:user_id>', methods=['GET'])
def get_all_tasks(user_id):
    
    filtered_tasks = ToDoList.query.filter_by(fk_user_id=user_id).all()

    tasks = []

    for task in filtered_tasks:
        tasks.append({"name": task.to_do_name,
                      "description": task.description,
                      "date": task.due_date,
                      "collection_id": task.fk_folder_id,
                        "status": task.status
                        })
        
    return jsonify(tasks)

@app.route('/api/task/all_from_collection/<int:collection_id>', methods=['GET'])
def get_all_tasks_from_collection(collection_id):
        
        filtered_tasks = ToDoList.query.filter_by(fk_folder_id=collection_id).all()
    
        tasks = []
    
        for task in filtered_tasks:
            tasks.append({"name": task.to_do_name,
                        "description": task.description,
                        "date": task.due_date,
                        "id": task.list_id,
                            "status": task.status
                            })
            
        return jsonify(tasks)


@app.route('/api/task/update/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    print("Updating a task")
    print(data)
    task = ToDoList.query.filter_by(list_id=task_id).first()

    task.to_do_name = data['name']
    task.description = data['description']
    task.due_date = data['date']
    task.fk_folder_id = data['collection_id']
    task.status = data['status']

    db.session.commit()

    return jsonify({"message": "Task updated!"})

@app.route('/api/task/delete/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
        
    task = ToDoList.query.filter_by(list_id=task_id).first()

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted!"})

@app.route('/api/task/<int:task_id>', methods=['GET'])
def get_task(task_id):
    
    task = ToDoList.query.filter_by(list_id=task_id).first()

    task = {"name": task.to_do_name,
            "description": task.description,
            "date": task.due_date,
            "collection_id": task.fk_folder_id,
            "status": task.status
            }

    return jsonify(task)

@app.route('/api/task/done/<int:task_id>', methods=['PUT'])
def mark_task_as_done(task_id):
    task = ToDoList.query.filter_by(list_id=task_id).first()

    task.status = True

    db.session.commit()

    return jsonify({"message": "Task marked as done!"})

@app.route('/api/task/undone/<int:task_id>', methods=['PUT'])
def mark_task_as_undone(task_id):
    task = ToDoList.query.filter_by(list_id=task_id).first()

    task.status = False

    db.session.commit()

    return jsonify({"message": "Task marked as undone!"})

# test route
@app.route('/api/test', methods=['GET'])
def test():
    print("Test successful!")
    return jsonify({"message": "Test successful!"})