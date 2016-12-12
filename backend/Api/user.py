from bottle import get, post, put, delete, request, response, redirect
from bottle import route, view
import datetime
import requests
import json
from bson import json_util
from bson import *
from bson.json_util import dumps

prefix = '/backend/Api'

# GET ====================================================================

def getUser(username):
    jsonFile = 'Api/users.json'
    with open(jsonFile) as data_file:    
        users = json.load(data_file) 
    for u in users:
        if u['username'] == username:
            return u     
    return None

def getFood():
    jsonFile = 'Api/food.json'
    food = []
    with open(jsonFile) as data_file:    
        food = json.load(data_file) 
    return food   

def getUsersFood(username):
    jsonFile = 'Api/user_food.json'
    user_food = []
    with open(jsonFile) as data_file:    
        user_food = json.load(data_file) 
    users_food_list =[]
    for uf in user_food:
        if uf['username'] == username:
            users_food_list.append(uf)
    return users_food_list 

def addFoodToUser(userFood):
    jsonFile = 'Api/user_food.json'
    user_food = []
    with open(jsonFile) as data_file:    
        user_food = json.load(data_file)   
    user_food.append(userFood)
    with open(jsonFile, 'w') as outfile:
        json.dump(user_food, outfile)
    
    
@post(prefix + '/user/login')
@post(prefix + '/User/login')
def get_users():
    try:
        jsonFile = 'Api/users.json'
        with open(jsonFile) as data_file:    
            users = json.load(data_file) 
        for u in users:
            if u['username'] == request.json['username']:
                response.set_cookie(request.json['username'], 'signed', path='/', domain=request.urlparts.hostname)
                return {'success': True, 'message': 'logged in'}       
        return {'success': False, 'message': 'user not found'}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@post(prefix + '/user/signup')
@post(prefix + '/User/signup')
def get_users():
    try:
        jsonFile = 'Api/users.json'
        with open(jsonFile) as data_file:    
            users = json.load(data_file) 
        for u in users:
            if u['username'] == request.json['username']:
                return {'success': False, 'message': 'user exists'}     
        
        users.append(request.json)
        with open(jsonFile, 'w') as outfile:
            json.dump(users, outfile)
        response.set_cookie(request.json['username'], 'signed', path='/', domain=request.urlparts.hostname)

        return {'success': True, 'message': 'user added'}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}



@get(prefix + "/user/<username>")
@get(prefix + "/User/<username>")
def get_user(username):
    try:
        user = getUser(username)
        return user
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/food")
@get(prefix + "/food")
def get_food():
    try:
        food = getFood()

        return {'list':food}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@post(prefix + "/user/<username>/food")
@post(prefix + "/user/<username>/food")
def add_food(username):
    try:
        tmp = {'username': username, 'food': request.json}
        addFoodToUser(tmp)
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/user/<username>/food")
@get(prefix + "/user/<username>/food")
def get_user_food(username):
    try:
        
        return {'list':getUsersFood(username)}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

