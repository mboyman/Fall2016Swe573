import os
import pytz
from pytz import timezone
from datetime import datetime
from bottle import get, post, request, response, redirect
from bottle import route, view
import requests
import jwt
import json
from bson import json_util
from bson import *
from bson.json_util import dumps
from Infrastructure.mongo_client import *
from Infrastructure.user_service import *
from Infrastructure.base_repository import *
import uuid
import random
import hashlib
from voluptuous import *

validate_user_post = Schema({
    Required('Email'): All(str, Length(min=1, max=50)),
    Required('UserName'): All(str, Length(min=1, max=50)),
    Required('Description', default=''): Any(None, str),
    Required('Timezone', default=''): Any(None, str),
    Required('FirstName', default=''): Any(None, str),
    Required('LastName', default=''): Any(None, str),
}, extra=ALLOW_EXTRA)

validate_user_property_post = Schema({
    Required('Type'): All(str, Length(min=1, max=50)),
    Required('Name'): All(str, Length(min=1, max=50)),
    Required('Value', default=''): Any(None, str),
    Required('IsPrivate', default=False): Any(None, bool),
}, extra=ALLOW_EXTRA)

class UserRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.f = {'PasswordHash': 0, 'PasswordSecurityStamp': 0}
        self.user_coll = self.db_client.user()
        self.device_user_assignment_coll = self.db_client.device_user_assignment()
        self.user_assignment_coll = self.db_client.user_assignment()

    def get(self, q=None, f=None):
        try:
            user_list = list(self.user_coll.find(q or {}, self.f.update(f) if f else self.f))
            return user_list
        except Exception as e:
            raise e

    def get_user(self, user_id):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            user = self.user_coll.find_one({'_id': user_id}, self.f)
            return user
        except Exception as e:
            raise e

    def add_user(self, user):
        try:
            user = validate_user_post(user)
            secStamp = uuid.uuid4()
            passHash = UserService.getSHA256Hash(UserService.generateRandomPassword(), secStamp)
            user['PasswordHash'] = passHash
            user['PasswordSecurityStamp'] = secStamp           
            res = self.user_coll.insert_one(user)
            return res
        except Exception as e:
            raise e            

    def update_user(self, user_id, _user):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            if not isinstance(_user['_id'], ObjectId):
                _user['_id'] = ObjectId(request.json['_id']['$oid'])
            user = self.user_coll.find_one({'_id': user_id})
            if user:
                user.update(_user)
                res = self.user_coll.update({'_id': user_id}, user)
                return res
        except Exception as e:
            raise e

    def delete_user(self, user_id):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)            
            self.device_user_assignment_coll.remove({'UserID': user_id})
            self.user_assignment_coll.remove({'$or': [{'ParentUserID': user_id}, {'ChildUserID': user_id}] })
            res = self.user_coll.delete_one({'_id': user_id})
            return res
        except Exception as e:
            raise e

    def add_user_property(self, user_id, user_property):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            user_property = validate_user_property_post(user_property)
            res = self.user_coll.update_one({'_id': user_id, '$or': [{'Properties.Name': {'$ne': user_property['Name']}}, {'Properties.Type': {'$ne': user_property['Type']}}]},
                                       {'$push': {'Properties': user_property}})
            return res
        except Exception as e:
            raise e

    def update_user_property(self, user_id, user_property):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            user_property = validate_user_property_post(user_property)
            res = self.user_coll.update_one({'_id': user_id, 'Properties': {'$elemMatch': {'Name': {'$eq': user_property['Name']}, 'Type': {'$eq': user_property['Type']}}}},
                                       {'$set': {'Properties.$.Value': user_property['Value'], 'Properties.$.IsPrivate': user_property['IsPrivate']}})
            return res
        except Exception as e:
            raise e
    
    def add_or_update_user_property(self, user_id, user_property):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            user_property = validate_user_property_post(user_property)
            res = self.user_coll.update_one({'_id': user_id, 'Properties': {'$elemMatch': {'Name': {'$eq': user_property['Name']}, 'Type': {'$eq': user_property['Type']}}}},
                                       {'$set': {'Properties.$.Value': user_property['Value'], 'Properties.$.IsPrivate': user_property['IsPrivate']}})
            if not res.matched_count and not res.modified_count:
                res = self.user_coll.update_one({'_id': user_id, '$or': [{'Properties.Name': {'$ne': user_property['Name']}}, {'Properties.Type': {'$ne': user_property['Type']}}]},
                                       {'$push': {'Properties': user_property}})
            return res
        except Exception as e:
            raise e

    def delete_user_property(self, user_id, user_property):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            res = self.user_coll.update_one({'_id': user_id}, {'$pull': {'Properties': user_property}})
            return res
        except Exception as e:
            raise e

    def add_user_roles(self, user_id, user_roles):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            res = self.user_coll.update_one({'_id': user_id}, {'$addToSet': {'Roles': {'$each': user_roles}}})
            return res
        except Exception as e:
            raise e

    def delete_user_roles(self, user_id, user_roles):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            res = self.user_coll.update_one({'_id': user_id}, {'$pull': {'Roles': {'$in': user_roles}}})
            return res
        except Exception as e:
            raise e

    def change_user_password(self, user_id, old_password, new_password=None):
        try:
            if not isinstance(user_id, ObjectId):
                user_id = ObjectId(user_id)
            
            user = self.user_coll.find_one({'_id':user_id})
            
            if user and user['PasswordHash'] == UserService.getSHA256Hash(old_password, user['PasswordSecurityStamp']):
                if not new_password :                
                    passHash = UserService.getSHA256Hash(UserService.generateRandomPassword(), user['PasswordSecurityStamp'])
                    user['PasswordHash'] = passHash
                    res = self.user_coll.update_one({'_id':user_id}, {'$set':{'PasswordHash': passHash}}  )
                if new_password:
                    passHash = UserService.getSHA256Hash(new_password, user['PasswordSecurityStamp'])
                    user['PasswordHash'] = passHash
                    res = self.user_coll.update_one({'_id':user_id}, {'$set':{'PasswordHash': passHash}}  )
                return res
        except Exception as e:
            raise e