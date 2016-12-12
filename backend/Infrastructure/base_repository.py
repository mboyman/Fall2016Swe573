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

class BaseRepository:
    def __init__(self):         
        self.db_client = MongoDBClient()

  