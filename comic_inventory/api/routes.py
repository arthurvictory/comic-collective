from flask import Blueprint, request, jsonify
from comic_inventory.helpers import token_required, random_quote_generator
from comic_inventory.models import db, Comic, comic_schema, comics_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
def getdata():
    return {'some': 'value'}


@api.route('/comics', methods = ['POST'])
@token_required
def create_comic(our_user):

    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    quality = request.json['quality']
    random_quote = random_quote_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    comic = Comic(name, description, price, quality, random_quote, user_token)

    db.session.add(comic)
    db.session.commit()

    response = comic_schema.dump(comic)

    return jsonify(response)

# Read 1 Single Drone Endpoint
@api.route('/comics/<id>', methods = ['GET'])
@token_required
def get_comic(our_user, id):
    if id:
        comic = Comic.query.get(id)
        response = comic_schema.dump(comic)
        return jsonify(response)
    else:
        return jsonify({'message': 'ID is missing'}), 401
    
# Read all the drones endpoint
@api.route('/comics', methods = ['GET'])
@token_required
def get_comics(our_user):
    token = our_user.token
    comics = Comic.query.filter_by(user_token = token).all()
    response = comics_schema.dump(comics)

    return jsonify(response)

# Update 1 Drone by ID
@api.route('/drones/<id>', methods = ['PUT'])
@token_required
def update_drone(our_user, id):
    comic = Comic.query.get(id)

    comic.name = request.json['name']
    comic.description = request.json['description']
    comic.price = request.json['price']
    comic.quality = request.json['quality']
    comic.random_quote = random_quote_generator()
    comic.user_token = our_user.token

    db.session.commit()

    response = comic_schema.dump(comic)

    return jsonify(response)

# Delete 1 Drone by ID
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_comic(our_user, id):
    comic = Comic.query.get(id)
    db.session.delete(comic)
    db.session.commit()

    response = comic_schema.dump(comic)

    return jsonify(response)