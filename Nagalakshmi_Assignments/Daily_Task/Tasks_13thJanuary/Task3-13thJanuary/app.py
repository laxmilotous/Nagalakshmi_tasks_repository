from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_url_path="")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("MYSQL_URL_PATTERN")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), index=False, unique=False, nullable=False)

    def __init__(self, department_id, name):
        self.id = department_id
        self.name = name


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/display-departments', methods=['POST'])
def display():
    id = request.form['id']
    name = request.form['name']
    department = Department(id, name)
    db.session.add(department)
    db.session.commit()
    departments = Department.query.all()
    # print(departments)
    return render_template('display.html', departments=departments)


if __name__ == '__main__':
    app.run(debug=True)
