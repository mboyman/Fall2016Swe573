import os
import pytz
from pytz import timezone
from datetime import datetime
from bottle import get, post, request, response ,redirect
from bottle import route, view
import requests
import jwt
import json
from bson import json_util
from bson import *
from bson.json_util import dumps
from Infrastructure.mongo_client import *
from Infrastructure.base_repository import *
import uuid
import random
import hashlib

class DeviceUserAssignmentRepository(BaseRepository):
    def __init__(self):         
        super().__init__()
        self.f = {'PasswordHash': 0, 'PasswordSecurityStamp': 0}
        self.device_user_assignment_coll = self.db_client.device_user_assignment() 
        self.user_coll = self.db_client.user() 
        self.device_coll = self.db_client.device() 
 
    def get_assigned_devices(self, user_id):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            device_id_list = [a['DeviceID'] for a in list(self.device_user_assignment_coll.find({'UserID': user_id}))]
            device_list = list(self.device_coll.find({'_id': {'$in': device_id_list}}, self.f))
            return device_list
        except Exception as e:
            raise e

    def get_parent_users(self, device_id):
        try:
            if not isinstance(device_id, ObjectId):
                device_id = ObjectId(device_id)
            user_id_list = [a['UserID'] for a in list(self.device_user_assignment_coll.find({'DeviceID': device_id}))]
            user_list = list(self.user_coll.find({'_id': {'$in': user_id_list}}, self.f))
            return user_list
        except Exception as e:
            raise e

    def is_assigned(self, user_id, device_id):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            if not isinstance(device_id, ObjectId):
                device_id = ObjectId(device_id)
            if self.device_user_assignment_coll.find_one({'UserID': user_id, 'DeviceID': device_id}):
                return True
            return False            
        except Exception as e:
            raise e
  
    def add_assignments(self, user_id, device_ids):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            docs = []
            for d in device_ids:
                if not isinstance(d, ObjectId):
                    d = ObjectId(d)
                docs.append({'UserID': user_id, 'DeviceID': d})
            return self.device_user_assignment_coll.insert_many(docs)
        except Exception as e:
            raise e

    def delete_assignments(self, user_id, device_ids):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)      
            device_oids = []
            for d in device_ids:
                if not isinstance(d, ObjectId):
                    d = ObjectId(d)  
                device_oids.append(d)    
            return self.device_user_assignment_coll.delete_many({"UserID" : user_id, 'DeviceID': {'$in': device_oids} })
        except Exception as e:
            raise e