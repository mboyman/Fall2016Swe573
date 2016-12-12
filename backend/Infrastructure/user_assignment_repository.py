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

class UserAssignmentRepository(BaseRepository):
    def __init__(self):         
        super().__init__()
        self.f = {'PasswordHash': 0, 'PasswordSecurityStamp': 0}
        self.user_assignment_coll = self.db_client.user_assignment() 
        self.user_coll = self.db_client.user() 

    def get(self, q, f):
        try:                      
            user_list = list(self.user_assignment_coll.find(q or {}, self.f.update(f) if f else self.f  ))
            return user_list
        except Exception as e:
            raise e

    def get_child_users(self, parent_user_id):
        try:
            if not isinstance(parent_user_id, ObjectId):
                parent_user_id = ObjectId(parent_user_id)
            child_id_list = [a['ChildUserID'] for a in list(self.user_assignment_coll.find({'ParentUserID': parent_user_id}))]
            user_list = list(self.user_coll.find({'_id': {'$in': child_id_list}}, self.f))
            return user_list
        except Exception as e:
            raise e

    def get_parent_users(self, child_user_id):
        try:
            if not isinstance(child_user_id, ObjectId):
                child_user_id = ObjectId(child_user_id)
            parent_id_list = [a['ParentUserID'] for a in list(self.user_assignment_coll.find({'ChildUserID': child_user_id }))]
            user_list = list(self.user_coll.find({'_id': {'$in': parent_id_list}}, self.f))
            return user_list
        except Exception as e:
            raise e

    def is_assigned(self, parent_user_id, child_user_id):
        try:
            if not isinstance(parent_user_id, ObjectId):
                parent_user_id = ObjectId(parent_user_id)
            if not isinstance(child_user_id, ObjectId):
                child_user_id = ObjectId(child_user_id)
            if self.user_assignment_coll.find_one({'ParentUserID': parent_user_id, 'ChildUserID': child_user_id }):
                return True
            return False            
        except Exception as e:
            raise e
  
    def add_assignment(self, parent_user_id, child_user_id):
        try:
            if not isinstance(parent_user_id, ObjectId):
                parent_user_id = ObjectId(parent_user_id)
            if not isinstance(child_user_id, ObjectId):
                child_user_id = ObjectId(child_user_id)
            return self.user_assignment_coll.insert_one({'ParentUserID': parent_user_id, 'ChildUserID': child_user_id})
        except Exception as e:
            raise e
  