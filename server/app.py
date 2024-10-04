# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    quake = Earthquake.query.get(id)
    if quake:
        return{
            "id": quake.id,
            "location": quake.location,
            "magnitude": quake.magnitude,
            "year": quake.year
        }, 200
    else:
        return {"message": f"Earthquake {id} not found."}, 404

# Add views here
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return ({
        "count": len(quakes),
        "quakes": [quake.to_dict() for quake in quakes]
    }), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
