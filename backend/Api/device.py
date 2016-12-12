from bottle import get, post, request, response ,redirect
from bottle import route, view
import datetime
import requests
import jwt
from pymongo import MongoClient
import pymongo
import json
from bson import json_util
from bson.json_util import dumps
from bson import *
from Infrastructure import *
from Infrastructure.auth import *
from Infrastructure.current_user import *
from Infrastructure.user_service import *
from voluptuous import *

prefix = '/backend/Api'

# validate_user_post = Schema({
#     Required('Email'): All(str, Length(min=1, max=50)), 
#     Required('UserName'): All(str, Length(min=1, max=50)), 
#     Required('Description', default = ''): Any(None, str), 
#     Required('Timezone', default = ''): Any(None, str), 
#     Required('FirstName', default = ''): Any(None, str), 
#     Required('LastName', default = ''): Any(None, str),        
#     }, extra=ALLOW_EXTRA)

validate_device_property_post = Schema({
    Required('Type'): All(str, Length(min=1, max=50)),    
    Required('Name'): All(str, Length(min=1, max=50)),    
    Required('Value', default = ''): Any(None, str),    
    Required('IsPrivate', default = False): Any(None, bool),        
    }, extra=ALLOW_EXTRA)

@get( prefix + '/device')
@get( prefix + '/Device')
def get_devices(start = 0, limit = 50):
    try:
        start = int(request.query.start or 1)
        lim = request.query.limit
        limit = None if lim and int(lim) == 0 else int(lim) if lim and int(lim) != None else 50
        device_coll = MongoDBClient().device()
        q = {}
        f = {}
        device_list = list(device_coll.find(q, f).skip(start).limit(limit))
    except Exception as e:
        device_list = []
    device_list = json.loads(json_util.dumps(device_list))
    return {
        "Start": start,
        "Limit": limit,
        "TotalCount": device_coll.find().count(),
        "List" :  device_list }


@get(prefix + "/device/<id>")
@get(prefix + "/device/<id>")
#@synapse_auth(['GlobalAdmin','Synapse-DeviceReader'])
def get_device(id):
    try:       
        client = MongoDBClient() 
        f = {}
        device = client.device().find_one({"_id": ObjectId(id) })               
        return json.loads(json_util.dumps(device))
    except Exception as e:
        pass

@get(prefix + "/device/<id>/status")
@get(prefix + "/device/<id>/Status")
#@synapse_auth(["GlobalAdmin","Synapse-DeviceReader"])
def get_device_status(id):
    try:
        client = MongoDBClient() 
        f = {}
        device_coll = MongoDBClient().device()
        device = device_coll.find_one({"_id": ObjectId(id) })        
        if device:
            device_status = client.device_status().find_one({"DeviceHWID": device['DeviceHWID'] })               
            return json.loads(json_util.dumps(device_status))            
        else:
            response.status = 404
            return {'success': False, 'message': 'Object Does Not Exist'}         
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e) }

@get(prefix + "/device/<id>/log")
@get(prefix + "/device/<id>/Log")
#@synapse_auth(["GlobalAdmin","Synapse-DeviceReader"])
def get_device_log(id):
    try:
        client = MongoDBClient() 
        f = {}
        device_coll = MongoDBClient().device()
        device = device_coll.find_one({"_id": ObjectId(id) })        
        if device:
            device_log = client.device_log().find_one({"DeviceHWID": device['DeviceHWID'] })               
            return json.loads(json_util.dumps(device_log))            
        else:
            response.status = 404
            return {'success': False, 'message': 'Object Does Not Exist'}         
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e) }

## POST 

@post(prefix + "/device")
@post(prefix + "/device")
@synapse_auth(["GlobalAdmin","Synapse-DeviceReader"])
def add_device():
    try:
        device = validate_device_post(request.json)
        device_coll = MongoDBClient().device()
        res = device_coll.insert_one(device)
        if res.acknowledged: 
            return json.loads(json_util.dumps(device_coll.find_one({'_id':res.inserted_id})))   
            pass     
    except Exception as e:
        pass


@post(prefix + "/device/<id>/property")
@post(prefix + "/device/<id>/property")
@synapse_auth(['GlobalAdmin','Synapse-DeviceReader'])
def add_property(id):
    try:
        device_property = validate_device_property_post(request.json)
        device_coll = MongoDBClient().device()        
        device = device_coll.find_one({"_id": ObjectId(id) })        
        if device:
            res = device_coll.update_one({'_id': device['_id'], '$or':[{'Properties.Name': {'$ne': device_property['Name']}},{'Properties.Type':{'$ne': device_property['Type']}}]}, 
                                {'$push': {'Properties': device_property} } )        
            if res.matched_count and res.modified_count:
                return {'success': True, 'message': 'Object Added'}            
        else:
            response.status = 404
            return {'success': False, 'message': 'Object Does Not Exist'}         
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e) }
