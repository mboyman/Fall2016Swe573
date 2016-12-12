import os
from datetime import datetime
from pytz import *
from bottle import get, post, request, response ,redirect
from bottle import route, view
import requests
import jwt
import json
from bson import json_util
from bson.json_util import dumps
from Infrastructure.mongo_client import *

server_secret = 'rebuslabssecret.*'

class CurrentUser:
    def __new__(cls):
        try:
            token = request.get_cookie("token")
            token = jwt.decode(token.encode('UTF-8'), server_secret,algorithm='HS256')
            user = MongoDBClient().user().find_one({"Email":token['email']}, {'PasswordHash':0, 'PasswordSecurityStamp': 0})
        except Exception as e:
            user = {}            
        return user
    
    @staticmethod
    def is_parent(child_id):
        user_assignment_coll = MongoDBClient().user_assignment()
        token = request.get_cookie("token")
        token = jwt.decode(token.encode('UTF-8'), server_secret,algorithm='HS256')
        user = MongoDBClient().user().find_one({"Email":token['email']}, {'PasswordHash':0, 'PasswordSecurityStamp': 0})
        res = user_assignment_coll.find_one({'ParentUserID': user['_id'], 'ChildUserID': child_id}) 
        if res:
            return True
        return False