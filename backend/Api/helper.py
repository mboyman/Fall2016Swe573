from bottle import get, post, request, response, redirect
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
from datetime import datetime, timedelta
from pytz import timezone, common_timezones
import pytz

client = MongoClient("mongodb://rebuslabsadmin:se-hd505@13.94.154.56:27017")
db = client.get_database("prod2-synapse-db")
collection = db.Device

prefix = '/backend/Api'


@route('/backend/Api/activedevicecount', method='GET')
def GetActiveDeviceCount():
    try:
        deviceCount = collection.find({}).count()
        response.content_type = 'application/json'
        documentToInsert = {
            "DeviceCount": deviceCount,
            "ActiveDeviceCount": deviceCount}
        return json.dumps(documentToInsert, default=json_util.default)
    except Exception as e:
        pass


@get(prefix + '/languages')
@get(prefix + '/Languages')
@synapse_auth([])
def get_site_languages():
    try:
        languages = [
            {
                "Key": "Türkçe",
                "Value": "tr-tr"
            },
            {
                "Key": "English(US)",
                "Value": "en-us"
            },
            {
                "Key": "Français(FR)",
                "Value": "fr-fr"
            }
        ]
        return {
            "Start": 1,
            "Limit": len(languages),
            "TotalCount": len(languages),
            'List': languages
        }
    except Exception as e:
        pass


@get(prefix + '/timezones')
@get(prefix + '/Timezones')
@synapse_auth([])
def get_timezones():
    try:
        return {
            "Start": 1,
            "Limit": len(common_timezones),
            "TotalCount": len(common_timezones),
            'List': [{'Key': tz, 'Value':tz} for tz in common_timezones]
        }
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}


@get(prefix + '/timezoneoffset')
@get(prefix + '/Timezoneoffset')
@synapse_auth([])
def get_timezone_offset():
    try:
        tz = timezone(request.query.tzone if request.query.tzone else 'UTC')
        return {
            'timezone': request.query.tzone,
            'timezoneoffset': datetime.now(tz).strftime('%z')
        }
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}

@get(prefix + '/propertytypes')
@get(prefix + '/Propertytypes')
@synapse_auth([])
def get_property_types():
    try:
        types = [
            'Address',
            'Coordinate',
            'File',
            'GeoFence',
            'Image',
            'Name',
            'NumberPlate',
            'PhoneNumber',
            'Tag',
            'Text',
            'URL',
        ]
        return {
            "Start": 1,
            "Limit": len(types),
            "TotalCount": len(types),
            'List': types
        }
    except Exception as e:
        response.status = 500
        return {'success': False, 'message': str(e)}