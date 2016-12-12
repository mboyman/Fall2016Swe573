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
from bson.json_util import dumps
from Infrastructure.mongo_client import *
import uuid
import random
import hashlib

class UserService:
    def __init__(self):         
        pass

    @staticmethod
    def createUser(ob):
        secStamp = uuid.uuid4()
        passHash = UserService.getSHA256Hash(UserService.generateRandomPassword(), secStamp)
        
        
    @staticmethod
    def generateRandomPassword():
        password = ""
        charSet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"     
        outGoingValue = None   
        for i in range(8):
            comingValue = random.randint(0, len(charSet)-1)
            if outGoingValue != comingValue and not (charSet[comingValue] in password or charSet[comingValue].upper() in password):
                password += charSet[comingValue]
            else:
                i=i-1
            outGoingValue = comingValue
        return password

    @staticmethod
    def getSHA256Hash(password, securityStamp):
        input = password + str(securityStamp)
        chekPass = hashlib.sha256(bytes(input, 'UTF-8')).hexdigest()
        return chekPass
