import os
import pytz
from pytz import timezone
from datetime import datetime
from bottle import get, post, request, response ,redirect
from bottle import route, view
import requests
import jwt
from pymongo import MongoClient
import pymongo
import json
from bson import json_util
from bson.json_util import dumps
from config import *

server_secret = 'rebuslabssecret.*'

class MongoDBClient:
    def __init__(self):         
        self.client = MongoClient(config["connectionstring-mongodbs"])
        self.db = self.client.get_database("prod2-synapse-db")
        self.db_log = self.client.get_database("prod2-synapse-log")
        
    def user(self):
        return self.db.User
        
    def device(self):
        return self.db.Device
    
    def device_status(self):
        return self.db.DeviceStatus

    def device_log(self):
        return self.db_log.DeviceLog

    def device_user_assignment(self):
        return self.db.DeviceUserAssignment

    def user_assignment(self):
        return self.db.UserAssignment
        
