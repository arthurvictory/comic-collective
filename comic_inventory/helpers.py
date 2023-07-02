from flask import request, jsonify
from functools import wraps
import secrets
import decimal
import requests
import json

from comic_inventory.models import User


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split()[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'}), 401
            
        except:
            our_user = User.query.filter_by(token=token).first()
            if token != our_user.token and secrets.compare_digest(token, our_user.token):
                return jsonify({'message': 'Token is invalid'}), 401
        return our_flask_function(our_user, *args, **kwargs)
    return decorated

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return json.JSONEncoder(JSONEncoder, self).default(obj)
    

def random_quote_generator():
    url = "https://famous-quotes4.p.rapidapi.com/random"

    querystring = {"category":"all","count":"2"}

    headers = {
        "X-RapidAPI-Key": "73c9a2e9f3mshb8e06bc4d900199p10e699jsn05beb9421bc1",
        "X-RapidAPI-Host": "famous-quotes4.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    data = response.json()

    return data[0]['author'] + ' ' + data[0]['text']