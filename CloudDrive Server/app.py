from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

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
    file_name = db.Column(db.String(20), unique=True, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    file_type = db.Column(db.String(20), nullable=False)
    file_url = db.Column(db.String(250), nullable=False)
    file_owner = db.Column(db.String(20), nullable=False)
    file_cloud_provider = db.Column(db.String(20), nullable=False)
    file_cloud_provider_api_key = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        # Return json representation of the object
        return f"File('{self.file_name}', '{self.file_size}', '{self.file_type}', '{self.file_path}', '{self.file_owner}', '{self.file_cloud_provider}', '{self.file_cloud_provider_api_key}')"


@app.route('/')
def index():
    return render_template("index.html")

# api endpoint to get all users
@app.route('/users/', methods=['GET'])
def get_all_users():
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
        return {"Please provide username and password."}
    username = request.json['username']
    password = request.json['password']
    # check if user exists
    user = UserDB.query.filter_by(username=username, password_hash=password).first()
    if user is not None:
        return {"status": "success",
                "message": "Login successful. Welcome!",
                "name": user.name, 
                "cloud_provider": user.cloud_provider, 
                "cloud_provider_api_key": user.cloud_provider_api_key, 
                "username": user.username, 
                "password": user.password_hash}
    else:
        return {"status": "fail",
                "message": "Loggin failed. Please check username and password."}


# api endpoint to register user
@app.route('/users/register/', methods=['GET', 'POST'])
def register_user():
    # if not request.json or not 'username' in request.json or not 'password' in request.json or not 'name' in request.json or not 'cloud_provider' in request.json or not 'cloud_provider_api_key' in request.json:
    #     return {"please provide required parameters."}

    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    cloud_provider = request.json['cloud_provider']
    cloud_provider_api_key = request.json['cloud_provider_api_key']

    # check if user exists
    user = UserDB.query.filter_by(username="username").first()
    if user is not None:
        return {"status": "user already exists."}
    else:
        # Insert New User in DB
        new_usr = UserDB(username=username, password_hash=password, name=name, cloud_provider=cloud_provider, cloud_provider_api_key=cloud_provider_api_key)
        db.session.add(new_usr)
        db.session.commit()
        
        return {"status": "success",
                "message": "User created successfully.",
                "name": name, 
                "cloud_provider": cloud_provider, 
                "cloud_provider_api_key": cloud_provider_api_key, 
                "username": username, 
                "password": password}

    
# fallback route for 404
@app.errorhandler(404)
def not_found(e):
    return "Wow! such a 404!"
 
# main driver function
if __name__ == '__main__':
    # create the database
    with app.app_context():
        db.create_all()
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)