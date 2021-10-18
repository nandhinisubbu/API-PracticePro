from flask import Flask, request
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///people.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

db.create_all()


@app.route('/api/person')
def get_person():
	Persons=Person.query.all()
	
	output=[]
	for person in Persons:
		person_data={'id': person.id,'first_name':person.first_name,'last_name':person.last_name}
		output.append(person_data)
	return {"Person":output}


@app.route('/api/person',methods=['POST'])
def add_person():
	person = Person(id=request.json['id'],first_name=request.json['first_name'],last_name=request.json['last_name'])
	db.session.add(person)
	db.session.commit()
	return{'id':person.id}


@app.route('/api/person',methods=['DELETE'])
def delete_person():
	person=Person.query.get(id)
	if person is None:
		return{"error":"not found"}
	db.session.delete(person)
	db.session.commit()
	return{"message"}
	

@app.route('/api/person',methods=['PUT'])
def edit_person():
	person=Person.query.get(id)
	person = Person(id,first_name=request.json['first_name'],last_name=request.json['last_name'])
	db.session.update(person)
	db.session.commit()
	return{'id':person.id}



api_manager = APIManager(app, flask_sqlalchemy_db=db)
api_manager.create_api(Person, methods=['GET', 'POST', 'DELETE', 'PUT'])

if __name__ == "__main__":
    app.run(debug = True)