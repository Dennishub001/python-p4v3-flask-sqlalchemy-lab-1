# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route("/earthquakes/<int:id>")
def get_earthquake(id: int):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    return make_response(jsonify({"message": "Earthquake 9999 not found."}), 404)

@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude: float):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    results = [eq.to_dict() for eq in earthquakes]
    return make_response(
        jsonify({
            "count": len(results),
            "quakes": results
        }),
        200
    )

if __name__ == '__main__':
    app.run(port=5555, debug=True)


