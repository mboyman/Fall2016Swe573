from bottle import get, post, put, delete, request, response, redirect
from bottle import route, view
import datetime
import requests
import json
from bson import json_util
from bson import *
from bson.json_util import dumps

prefix = '/backend/Api'
api_key = 'mGKWC6iiQy5XABlrCzmJp5Qpyw6HUPByfnu2AT1I'

# GET ====================================================================

def getUser(username):
    jsonFile = 'Api/users.json'
    with open(jsonFile, encoding='utf-8') as data_file:    
        users = json.load(data_file) 
    for u in users:
        if u['username'] == username:
            return u     
    return None

def getExercises():
    jsonFile = 'Api/Exercises.json'
    with open(jsonFile, encoding='utf-8') as data_file:    
        exercises = json.load(data_file)    
    return exercises

def getFood(q):
    q['api_key'] = api_key
    r = requests.get('http://api.nal.usda.gov/ndb/search', params=q)
    food = r.json()    
    return food   

def getUsersFood(username):
    jsonFile = 'Api/user_food.json'
    user_food = []
    with open(jsonFile, encoding='utf-8') as data_file:    
        user_food = json.load(data_file) 
    users_food_list =[]
    for uf in user_food:
        if uf['username'] == username:
            users_food_list.append(uf)
    return users_food_list 

def getUsersExercises(username):
    jsonFile = 'Api/user_exercise.json'
    exercises = []
    with open(jsonFile, encoding='utf-8') as data_file:    
        exercises = json.load(data_file) 
    user_exercise_list =[]
    for ex in exercises:
        if ex['username'] == username:
            user_exercise_list.append(ex)
    return user_exercise_list

def getFoodNutrients(q):
    q['api_key'] = api_key
    r = requests.get('http://api.nal.usda.gov/ndb/reports/', params=q)
    return r.json() 
    

def addFoodToUser(userFood):
    jsonFile = 'Api/user_food.json'
    user_food = []
    with open(jsonFile, encoding='utf-8') as data_file:    
        user_food = json.load(data_file)   
    user_food.append(userFood)
    with open(jsonFile, 'w', encoding='utf-8') as outfile:
        json.dump(user_food, outfile)

def addExerciseToUser(ex):
    jsonFile = 'Api/user_exercise.json'
    user_exercise = []
    with open(jsonFile, encoding='utf-8') as data_file:    
        user_exercise = json.load(data_file)   
    user_exercise.append(ex)
    with open(jsonFile, 'w', encoding='utf-8') as outfile:
        json.dump(user_exercise, outfile)
    
@post(prefix + '/user/login')
@post(prefix + '/User/login')
def get_users():
    try:
        jsonFile = 'Api/users.json'
        with open(jsonFile, encoding='utf-8') as data_file:    
            users = json.load(data_file) 
        for u in users:
            if u['username'] == request.json['username']:
                dom = request.urlparts.hostname if 'localhost' in request.urlparts.hostname else request.urlparts.hostname+':8080'
                response.set_cookie(request.json['username'], 'signed', path='/', domain=request.urlparts.hostname)
                return {'success': True, 'message': 'logged in', 'domain': dom}       
        return {'success': False, 'message': 'user not found'}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@post(prefix + '/user/logout')
def logout():
    try:
        username = request.json['username']
        response.delete_cookie(username, path='/')
        return {'success': True, 'redirect': 'http://'+request.urlparts.hostname+':8080'+'/static/index.html#/login'}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': ''}

@post(prefix + '/user/signup')
@post(prefix + '/User/signup')
def get_users():
    try:
        jsonFile = 'Api/users.json'
        with open(jsonFile, encoding='utf-8') as data_file:    
            users = json.load(data_file) 
        for u in users:
            if u['username'] == request.json['username']:
                return {'success': False, 'message': 'user exists'}     
        
        users.append(request.json)
        with open(jsonFile, 'w', encoding='utf-8') as outfile:
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

@get(prefix + "/exercises")
def get_food():
    try:
        exercises = getExercises()
        return {'list':exercises}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/food")
@get(prefix + "/food")
def get_food():
    try:
        ob = {
            'q': request.query.q,
            'format':'json',
            'sort':'n',
            'max': 1000,
            'offset':0
        }

        food = getFood(ob)

        return {'list':food}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/food/<ndbno>/nutrient")
@get(prefix + "/food/<ndbno>/nutrient")
def get_food(ndbno):
    try:
        nutrient = getFoodNutrients({'ndbno': ndbno})
        return nutrient
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

@post(prefix + "/user/<username>/exercises")
def add_exercises(username):
    try:
        tmp = {'username': username, 'exercise': request.json}
        addExerciseToUser(tmp)
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/user/<username>/food")
def get_user_food(username):
    try:
        
        return {'list':getUsersFood(username)}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + "/user/<username>/exercise")
def get_user_exercises(username):
    try:
        
        return {'list':getUsersExercises(username)}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

