from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

# Dummy Admin
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    desc = db.Column(db.String(200))
    image = db.Column(db.String(200))

# LOGIN API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == ADMIN_USER and data['password'] == ADMIN_PASS:
        return jsonify({'status':'success'})
    return jsonify({'status':'fail'})

# ADD PROJECT WITH IMAGE
@app.route('/add', methods=['POST'])
def add_project():
    title = request.form['title']
    desc = request.form['desc']
    image = request.files['image']

    path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(path)

    project = Project(title=title, desc=desc, image=path)
    db.session.add(project)
    db.session.commit()

    return jsonify({'message':'Added'})

# GET PROJECTS
@app.route('/projects')
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {'title':p.title,'desc':p.desc,'image':p.image}
        for p in projects
    ])

if __name__ == '__main__':
    import os
    os.makedirs('uploads', exist_ok=True)

    with app.app_context():
        db.create_all()

    app.run(debug=True)