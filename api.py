#flask api
import requests
from flask import Flask, session, request, jsonify
import json
from config import config
from request import ModelRequest
from functools import wraps
from datetime import datetime as dt

api = Flask(__name__)
conf = config()
iaRequest = ModelRequest(host=conf.ia_ip,port=conf.ia_port,argsList=['ingridents','r2'],resource='createRecipe')

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
    username = request.form['username']
    password = request.form['password']
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
    ingredients = request.form['ingredients']
    r2 = requests.form['determination']
    response = iaRequest.request([ingredients,r2])
    if response.status_code == 200:
        #if the request was successful send the result formatted to flutter
        return response.json(), 200 # TODO: format the response to flutter
    else:
        return jsonify({'message': 'Internal server error'}), 500

@api.route('/insert_recipe_db', methods=['GET'])
@login_required
def insertRecipeDB(): # add a recipe to the user collection of recipes
    name = request.header.get('name')
    date = dt.now()
    ingredients = request.header.get('ingredients')
    #TODO: add recipe to user collection of recipes
    return jsonify({'message': 'recipe inserted'}), 200

@api.route('/get_recipe_db', methods=['GET'])
@login_required
def getRecipeDB(): # get all the recipes of the user
    user = request.header.get('user')
    #TODO: get all the recipes of the user in the mongo database
    result = []
    return jsonify({'message': result}), 200
    
    