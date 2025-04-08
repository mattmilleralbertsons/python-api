from flask import Flask, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database connection. Replace with your database details
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLite example
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a simple model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), unique=False, nullable=False)
    
    def __init__(self, first_name):
        self.first_name = first_name

    def __repr__(self):
        return f'<User {self.id}>'
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name
        }

# Create all database tables if they don't exist
with app.app_context():
    db.create_all()

    #Add a default user
    if Person.query.filter_by(first_name='matt').first() is None:
        print("Creating person 'matt'")
        new_user = Person(first_name='matt')
        db.session.add(new_user)
        db.session.commit()
        
    if Person.query.filter_by(first_name='chris').first() is None:
        print("Creating person 'chris'")
        new_user = Person(first_name='chris')
        db.session.add(new_user)
        db.session.commit()

@app.route('/people/<int:person_id>')
def get_person_by_id(person_id):
    # Query the database for the user
    person = Person.query.get(person_id)
    if person:
        return person.to_dict()
    else:
        return abort(404, description="Person not found")

if __name__ == '__main__':
    app.run(debug=True)