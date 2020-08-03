import logging
from flask import Flask, jsonify, request
from typing import List
from marshmallow import ValidationError
from models.beer import Beer
from schemas.beer import CreateBeerSchema, BeerResponseSchema
from pubsub.publication import send_notification

logger = logging.getLogger()
logger.setLevel(logging.ERROR)
app = Flask(__name__)

beers: List[Beer] = list()


@app.route('/beers')
def get_root():
    try:
        return jsonify({'beers': [BeerResponseSchema().dump(b) for b in beers]})
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Something Went Wrong"}), 500


@app.route('/beers', methods=['POST'])
def add_beer():
    try:
        beer: Beer = CreateBeerSchema().load(request.json)
        beers.append(beer)
        send_notification(beer)
        beer_response = BeerResponseSchema().dump(beer)
        return jsonify({'player': beer_response}), 200
    except ValidationError as err:
        return jsonify({"message": "Invalid Request", "details": err.messages}), 400
    except Exception as e:
        logging.error(e)
        return jsonify({"message": "Something Went Wrong"}), 500


if __name__ == '__main__':
    app.run(debug=True)
