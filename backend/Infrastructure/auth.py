from bottle import get, post, request, response
from bottle import route, view
from datetime import *
import requests
import jwt
from pymongo import MongoClient
import pymongo
import json
import bson
from bson import json_util
from bson.json_util import dumps
from Infrastructure.current_user import *
from config import *

mainhost = "prod2-synapse.rebuslabs.com"
server_secret = 'rebuslabssecret.*'

def token_generator(email):    
    token = jwt.encode({'email': email , 'exp':datetime.utcnow() + timedelta(seconds=900) }, server_secret, algorithm='HS256')
    hostname = '.rebuslabs.com'
    if request.urlparts.hostname == 'localhost':
        hostname = request.urlparts.hostname
    response.set_cookie("synapseapicookie", "signed", path='/', domain = hostname, httponly=True)
    response.set_cookie("token", token.decode('UTF-8'), path='/', domain = hostname, httponly=True)
    return True

def isAuthorized(roles):
    try:
        synapseapicookie = request.get_cookie("synapseapicookie")
        token = request.get_cookie("token")
        if synapseapicookie and token:
            decodedToken = jwt.decode(token.encode('UTF-8'), server_secret,algorithm='HS256')            
            hostname = '.rebuslabs.com'
            if request.urlparts.hostname == 'localhost':
                hostname = request.urlparts.hostname
            if len(roles) == 0:
                decodedToken["exp"] = datetime.utcnow() + timedelta(seconds=900)                    
                response.set_cookie("token", jwt.encode(decodedToken, server_secret, algorithm='HS256').decode('UTF-8'), path='/', domain = hostname, httponly=True)
                return {"success": True, "message": "Authorized" }
            currentUser = CurrentUser()
            for role in roles:
                if role in currentUser['Roles']:
                    decodedToken["exp"] = datetime.utcnow() + timedelta(seconds=900)
                    response.set_cookie("token", jwt.encode(decodedToken, server_secret, algorithm='HS256').decode('UTF-8'), path='/', domain = hostname, httponly=True)
                    return {"success": True, "message": "Authorized" }
            return {"success": False, "message": "Not Authorized" }
        else:
            return {"success": False, "message": "Not Authenticated" }
    except (jwt.ExpiredSignatureError,jwt.DecodeError) as e:
        return {"success": False, "message": "Not Authenticated" }

def synapse_auth(argument):
    def decorator(function):
        def wrapper(*args, **kwargs):
            ob = isAuthorized(argument)  
            if  ob['success']: 
                return function(*args, **kwargs)
            else:
                hostname = config['hostname']
                if ob['message'] == 'Not Authorized':
                    response.status = 401
                    ob['redirect'] = 'http://' + hostname + ':8085/static/index.html'
                else:
                    response.status = 403
                    ob['redirect'] = 'http://' + hostname + ':8084/static/index.html#/login'
                return ob
        return wrapper
    return decorator


