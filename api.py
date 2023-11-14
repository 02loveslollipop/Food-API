#flask api
import requests
from flask import Flask, request, jsonify
import json
from config import config
from request import ModelRequest
from functools import wraps
from datetime import datetime as dt
from pymongo import MongoClient
from flask_cors import CORS
import hashlib
import pandas as pd

api = Flask(__name__)
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
conf = config()
iaRequest = ModelRequest(host=conf.ia_ip,port=conf.ia_port,argsList=['ingredients'],resource='request')
db = MongoClient()
session = []

def connect_to_database():
    client = MongoClient(conf.mongo_uri)
    return client[conf.mongo_db]

def login_required(func): # Wrapper to check if the user is in session if required
    @wraps(func)
    def wrapper(*args, **kwargs):
        username_hash = request.headers.get('secretAuth')
        if username_hash not in session:
            return jsonify({'message': 'user not in session'}), 401
        return func(*args, **kwargs)
    return wrapper

def checkPassword(username,password) -> bool: # check if the password is correct
    database = connect_to_database()
    users_collection = database['Usr']
    user = users_collection.find_one({'name': username})
    if not user:
        return False
    
    hashed_password = user['_password']
        
    if f"{password}" == f"{hashed_password}":
        return True
    else:
        return False

@api.route('/login', methods=['GET'])
def login(): #Add user to session
    username = request.headers.get('username')
    password = request.headers.get('password')
    
    if checkPassword(username,password):
        username_hash = hashlib.sha256((username + dt.now.__str__()).encode()).hexdigest()
        session.append(username_hash)
        return jsonify({'secretAuth': username_hash}), 200
    else:
        return jsonify({'message': 'login failed'}), 401

@api.route('/logout')
@login_required
def logout(): #Remove user from session
    username_hash = request.headers.get('hash')
    session.pop(username_hash)
    return jsonify({'message': 'logout successful'}), 200

@api.route('/create_recipe', methods=['GET'])
@login_required
def createRecipe(): # request a recipe inference to the IA model
    ingredients = request.headers.get('ingredients') #The ingredinetes are passed as a vector of strings
    response = iaRequest.request([ingredients]) #Send the request to the IA model
    if response.status_code == 200: #If the request was successful
        return response.json(), 200
    else:
        return jsonify({'message': "This didn't work as expected :("}), 500 #TODO: search a less silly message

@api.route('/insert_recipe_db', methods=['GET'])
@login_required
def addToFavoriteDB():
    username = request.headers.get('username')
    name = request.headers.get('name')
    url = request.headers.get('url')
    print(username)
    print(name)
    print(url)
    database = connect_to_database()
    users_collection = database['Usr']
    user = users_collection.find_one({'name': username})
    if not user:
        return jsonify({'message': 'user not found'}), 401

    users_collection.update_one({'name': username}, {'$push': {'likedRecipes': {'recipe_name': name, 'recipe_urls': url}}})
    
    return jsonify({'message': 'added to favorite recipes of the user :)'}), 200 #TODO: search a less silly message

@api.route('/get_recipe_db', methods=['GET'])
@login_required
def getRecipeDB(): # get all the recipes of the user
    username = request.headers.get('user')
    
    #the collection have an array of objects (that are the recipes) that is called likedRecipes, the objects have 2 fields: recipe_name and recipe_urls, when called this function, the function will extract the array of objects and return it as a json

    database = connect_to_database()
    users_collection = database['Usr']
    recipes = users_collection.find_one({'name': username})
    if not recipes:
        return jsonify({'message': 'user not found'}), 401
    
    response = recipes['likedRecipes']
    response.pop(0)
    responseDataframe = pd.DataFrame(response).to_json(orient='records')
    return responseDataframe, 200   

if __name__ == '__main__':
    api.run(debug=True, host='0.0.0.0', port=6970)