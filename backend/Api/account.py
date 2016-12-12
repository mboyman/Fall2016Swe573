from bottle import get, post, put, request, response ,redirect
from bottle import route, view
import datetime
import requests
import jwt
from pymongo import MongoClient
import pymongo
import json
from bson import json_util
from bson.json_util import dumps
from Infrastructure import auth
from Infrastructure.auth import *
from Infrastructure.current_user import *
from Infrastructure.user_repository import *

prefix = '/backend/Api'

@get(prefix + '/account')
@get(prefix + '/Account')
@synapse_auth([])
def account():
    try:
        account = CurrentUser()
        return json.loads(json_util.dumps(account))
    except Exception as e:
        pass



@post('/backend/Api/account/Login')
@post('/backend/Api/account/login')
def login():
    try:
        password = request.json["password"]
        username = request.json["username"]
        if(password == "se-hd505" and username == "admin@rebuslabs.com"):
            auth.token_generator(username)
            return "Success!"
        else:
            return "Error"
    except Exception as e:
        pass

@get('/account/Login')
@get('/Account/login')
@synapse_auth(['GlobalAdmin'])
def login():

    return redirect('/login')

@get('/backend/Api/account/Logout')
@get('/backend/api/account/logout')
def logout():
    response.set_cookie('token',expires=0)
    return {'success': True, 'redirect':'http://localhost:8084/static/index.html#/login'}


@route('/backend/Api/account', method='GET')
def GetActiveDeviceCount():
    try:            
        user = CurrentUser()
        return json.dumps(user, default=json_util.default)
    except Exception as e:
        pass


@put(prefix + "/account")
@put(prefix + "/Account")
@synapse_auth([])
def update_account():
    try:
        current_user = CurrentUser()
        if ObjectId(request.json['_id']['$oid']) == current_user['_id']:
            res = UserRepository().update_user(current_user['_id'], request.json)
            if res['nModified']:
                return {'success': True, 'message': 'Object Modified'}
        else:
            response.status = 404
            return {'success': False, 'message': 'Object Does Not Exist'}
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}