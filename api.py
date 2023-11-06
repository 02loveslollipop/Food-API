#flask api
import requests
from flask import Flask, session, request, jsonify
import json
from config import config
from request import ModelRequest
from functools import wraps
from datetime import datetime as dt
from pymongo import MongoClient
from flask_cors import CORS

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
conf = config()
iaRequest = ModelRequest(host=conf.ia_ip,port=conf.ia_port,argsList=['ingredients'],resource='request')
db = MongoClient(conf.mongo_uri)
api.secret_key = conf.flask_secret

def login_required(func): # Wrapper to check if the user is in session if required
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'user not in session'}), 401
    return wrapper

def checkPassword(username,password) -> bool: # check if the password is correct
    #TODO: check password in the mongo database
    return True

@api.route('/login', methods=['GET'])
def login(): #Add user to session
    username = request.headers.get('username')
    password = request.headers.get('password')
    #TODO:delete from here when the mongo database is ready
    if username == 'test' and password == 'test':
        session['username'] = username
        print("Login successful")
        return jsonify({'message': 'login successful'}), 200
        
    else:
        return jsonify({'message': 'login failed'}), 401
    #TODO: to here
    if checkPassword(username,password):
        session['username'] = username
        return jsonify({'message': 'login successful'}), 200
    else:
        return jsonify({'message': 'login failed'}), 401

@api.route('/logout')
@login_required
def logout(): #Remove user from session
    session.pop('username', None)
    return jsonify({'message': 'logout successful'}), 200

@api.route('/create_recipe', methods=['GET'])
@login_required
def createRecipe(): # request a recipe inference to the IA model
    ingredients = request.form['ingredients'] #The ingredinetes are passed as a vector of strings
    ingredients = ','.join(ingredients) #Convert the list to a string separated by commas
    response = iaRequest.request([ingredients]) #Send the request to the IA model
    if response.status_code == 200: #If the request was successful
        return response.json(), 200
    else:
        return jsonify({'message': "This didn't work as expected :("}), 500 #TODO: search a less silly message

@api.route('/insert_recipe_db', methods=['GET'])
@login_required
def addToFavoriteDB():
    user = request.header.get('user')
    name = request.header.get('name')
    url = request.header.get('url')
    date = dt.now()
    #TODO: add recipe to user collection of recipes
    return jsonify({'message': 'added to favorite recipes of the user :)'}), 200 #TODO: search a less silly message

@api.route('/get_recipe_db', methods=['GET'])
@login_required
def getRecipeDB(): # get all the recipes of the user
    user = request.header.get('user')
    #TODO: get all the recipes of the user in the mongo database
    result = []
    return jsonify({'message': result}), 200
    
if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=6970)
