from urllib import response
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserDB(db.Model):
    """
    This class creates the User table in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    cloud_provider = db.Column(db.String(20), nullable=False)
    cloud_provider_api_key = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        # Return json representation of the object
        return f"User('{self.username}', '{self.name}', '{self.cloud_provider}')"
    
    
class FilesDB(db.Model):
    """
    This class creates the Files table in the database.
    """
    id = db.Column(db.Integer, primary_key=True)
    file_owner = db.Column(db.Integer, nullable=False)
    file_name = db.Column(db.String(20), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    file_url_pub = db.Column(db.String(250), nullable=False)
    file_url_pvt = db.Column(db.String(500), nullable=False)
    file_handle = db.Column(db.String(100), nullable=False)
    file_status = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        # Return json representation of the object
        return f"File('{self.file_name}', '{self.file_size}', '{self.file_type}', '{self.file_path}', '{self.file_owner}', '{self.file_cloud_provider}', '{self.file_cloud_provider_api_key}')"


@app.route('/')
def index():
    return render_template("index.html")


# api endpoint to get all users
@app.route('/users/', methods=['GET'])
def get_all_users():
    # authenticate user
    if not request.json or not 'cloud_provider_api_key' in request.json:
        return {"status": "fail",
                "message": "Missing Parameters"}
    else:
        cloud_provider_api_key = request.json['cloud_provider_api_key']
        # check if user exists
        user = UserDB.query.filter_by(cloud_provider_api_key=cloud_provider_api_key).first()
        if user is None:
            return {"status": "fail",
                    "message":  "Authentication Failed"}
        
    # get all users after authentication
    users = UserDB.query.all()
    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['password_hash'] = user.password_hash
        user_data['name'] = user.name
        user_data['cloud_provider'] = user.cloud_provider
        user_data['cloud_provider_api_key'] = user.cloud_provider_api_key
        output.append(user_data)
    return {"users": output}


# api endpoint to auth user login
@app.route('/users/login/', methods=['GET', 'POST'])
def auth_user_login():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return {"message":"Missing Parameters",
                "status":"fail"}
    username = request.json['username'].strip()
    password = request.json['password'].strip()
    # check if user exists
    user = UserDB.query.filter_by(username=username, password_hash=password).first()
    if user is not None:
        return {"status": "success",
                "message": "Login Successful",
                "id": user.id,
                "name": user.name, 
                "cloud_provider": user.cloud_provider, 
                "cloud_provider_api_key": user.cloud_provider_api_key, 
                "username": user.username, 
                "password": user.password_hash}
    else:
        return {"status": "fail",
                "message": "Login Failed, try again"}


# api endpoint to register user
@app.route('/users/register/', methods=['GET', 'POST'])
def register_user():
    username = request.json['username'].strip()
    password = request.json['password'].strip()
    name = request.json['name'].strip()
    cloud_provider = request.json['cloud_provider'].strip()
    cloud_provider_api_key = request.json['cloud_provider_api_key'].strip()
    # check if user exists
    user = UserDB.query.filter_by(username=username).first()
    if user is not None:
        return {"status": "User Already Exists, Select another Username"}
    else:
        # Insert New User in DB
        new_usr = UserDB(
            username=username, password_hash=password, 
            name=name, cloud_provider=cloud_provider, 
            cloud_provider_api_key=cloud_provider_api_key.strip()
        )
        db.session.add(new_usr)
        db.session.commit()
        new_usr = UserDB.query.filter_by(username=username, password_hash=password).first()
        return {"status": "success",
            "message": "Registration Successful",
            "id": new_usr.id,
            "name": name, 
            "cloud_provider": cloud_provider, 
            "cloud_provider_api_key": cloud_provider_api_key, 
            "username": username, 
            "password": password}


# api endpoint to get all files
@app.route('/files/', methods=['POST'])
def get_all_files():
    # authenticate user
    if not request.json or not 'file_owner' in request.json or not 'cloud_provider_api_key' in request.json:
        return {"status": "fail",
                "message": "Missing Parameters"}
    else:
        file_owner = request.json['file_owner']
        cloud_provider_api_key = request.json['cloud_provider_api_key']
        # check if user exists
        user = UserDB.query.filter_by(id=file_owner, cloud_provider_api_key=cloud_provider_api_key).first()
        if user is None:
            return {"status": "fail",
                    "message":  "Authentication Failed"}
    # get the files of the user after authentication
    file_owner = request.json['file_owner']
    cloud_provider_api_key = request.json['cloud_provider_api_key']
    files = FilesDB.query.filter_by(file_owner=file_owner).all()
    # check if files exists
    if files is None:
        return {"status": "fail",
                "message": "Files Retrieval Failed"}
    output = []
    # create the json response
    for file in files:
        file_data = {}
        file_data['id'] = file.id
        file_data['file_owner'] = file.file_owner
        file_data['file_name'] = file.file_name
        file_data['file_size'] = file.file_size
        file_data['file_type'] = file.file_type
        file_data['file_url'] = file.file_url_pub
        file_data['file_handle'] = file.file_handle
        file_data['file_status'] = file.file_status
        output.append(file_data)
    return {"files": output,
            "status": "success",
            "message": "Files Retrieved Successfully"}


# api endpoint to upload file
@app.route('/files/upload/', methods=['GET', 'POST'])
def upload_file():
    # authenticate user
    if not request.json or not 'file_owner' in request.json or not 'file_name' in request.json or not 'file_size' in request.json or not 'file_type' in request.json or not 'file_url_pub' in request.json or not 'file_handle' in request.json or not 'file_status' in request.json:
        return {"status" : "fail",
            "message" : "Missing Parameters"
        }
    else:
        file_owner = request.json['file_owner']
        cloud_provider_api_key = request.json['cloud_provider_api_key']
        # check if user exists
        user = UserDB.query.filter_by(id=file_owner, cloud_provider_api_key=cloud_provider_api_key).first()
        if user is None:
            return {"status" : "fail",
                "message" :  "Authentication Failed"
            }
    # get the file parameters after authentication
    file_name = request.json['file_name'].strip()
    file_owner = request.json['file_owner']
    file_size = request.json['file_size']
    file_type = request.json['file_type'].strip()
    file_url_pub = request.json['file_url_pub'].strip()
    file_url_pvt = request.json['file_url_pvt'].strip()
    file_handle = request.json['file_handle'].strip()
    file_status = request.json['file_status'].strip()
    # Insert New File in DB
    new_file = FilesDB(
        file_owner=file_owner, file_name=file_name, 
        file_size=file_size, file_type=file_type, 
        file_url_pub=file_url_pub, file_url_pvt=file_url_pvt,
        file_handle=file_handle, file_status=file_status
    )
    db.session.add(new_file)
    db.session.commit()
    return {"status" : "success",
        "message": "File Uploaded Successfully"}


@app.route('/files/upload/check/', methods=['POST'])
def check_upload():
    # check if file exists
    file_name = request.json['file_name'].strip()
    file_owner = request.json['file_owner']

    file = FilesDB.query.filter_by(file_name=file_name, file_owner=file_owner).first()
    if file is not None:
        return {"status" : "success",
            "file_exists" : "True",
            "message" : "File Already Exists"
        }
    return {"status" : "fail",
        "file_exists" : "False",
        "message" : "File Does Not Exist"
    }

# fallback route for 404
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")
 

# main driver function
if __name__ == '__main__':
    # create the database
    with app.app_context():
        db.create_all()
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)