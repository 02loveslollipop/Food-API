#flask api
import requests
from flask import Flask, session, request, jsonify
import json
from config import config
from request import ModelRequest
from functools import wraps

api = Flask(__name__)
conf = config()
iaRequest = ModelRequest(host=conf.ia_ip,port=conf.ia_port,argsList=['ingridents','r2'],resource='createRecipe')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'user not in session'}), 401
    return wrapper

def checkPassword(username,password) -> bool:
    #TODO: check password in the sql database
    return True

@api.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if checkPassword(username,password):
        session['username'] = username
        return jsonify({'message': 'login successful'}), 200
    else:
        return jsonify({'message': 'login failed'}), 401

@api.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    return jsonify({'message': 'logout successful'}), 200

@api.route('/createRecipe', methods=['POST'])
@login_required
def createRecipe():
    ingredients = request.form['ingredients']
    r2 = requests.form['determination']
    response = iaRequest.request([ingredients,r2])
    if response.status_code == 200:
        #TODO: if request is successful, save recipe in the sql database, and return the formated result to send to flutter
        resultData = "" #Formated result to send to flutter
        return jsonify({'message': resultData}), 200
    else:
        return jsonify({'message': 'Internal server error'}), 500

@api.route('/retrieveFoodRequestByUser', methods=['POST'])
@login_required
def retrieveFoodRequestByUser():
    username = session['username']
    #TODO: retrieve food request from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200

@api.route('/retrieveFoodRequestDescriptionByID', methods=['POST'])
@login_required
def retrieveFoodRequestDescriptionByID():
    id = request.form['id']
    #TODO: retrieve food request from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200

@api.route('/RetrieveIngredientByID', methods=['POST'])
@login_required
def RetrieveIngredientByID():
    id = request.form['id']
    #TODO: retrieve ingredient from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200

@api.route('/RetrieveAllIngredients', methods=['POST'])
@login_required
def RetrieveAllIngredients():
    #TODO: retrieve all ingredients from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200

@api.route('/RetrieveAllRecipes', methods=['POST'])
@login_required
def RetrieveAllRecipes():
    #TODO: retrieve all recipes from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200

@api.route('/RetrieveRecipeByID', methods=['POST'])
@login_required
def RetrieveRecipeByID():
    id = request.form['id']
    #TODO: retrieve recipe from sql database
    resultData = ""
    return jsonify({'message': resultData}), 200
    


