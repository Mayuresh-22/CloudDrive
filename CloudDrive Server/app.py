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
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.age}')"
    

@app.route('/')
def index():
    return render_template("index.html")

# api endpoint to fetch users with id, make id parameter optional
@app.route('/users/<id>', methods=['GET'])
def get_users(id=None):
    if id:
        user = UserDB.query.filter_by(id=id).first()
        if user is not None:
            return f"User: {user.name} is {user.age} years old."
        else:
            return "User Not found"
    else:
        return "All users."

# api endpoint to add a user
@app.route('/users/add/', methods=['GET'])
def add_user():
    if not request.args.get("name") or not request.args.get("age"):
        return "Please provide name and age."
    db.session.add(UserDB(name=request.args.get("name"), age=request.args.get("age")))
    db.session.commit()
    return f"User: {request.args.get('name')} added."

# api endpoint to auth user login
@app.route('/users/login/', methods=['GET', 'POST'])
def auth_user_login():
    if not request.json or not 'username' in request.json or not 'password' in request.json:
        return {"Please provide username and password."}
    username = request.json['username']
    password = request.json['password']
    if username == "admin" and password == "admin":
        return {"status": "success"}
    else:
        return {"status": "failed"}

# fallback route for 404
@app.errorhandler(404)
def not_found(e):
    return "Wow! such a 404!"
 
# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run(debug=True)