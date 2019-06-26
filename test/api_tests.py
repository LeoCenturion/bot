import unittest
import sys
sys.path.append('../')
import bots
import mock
import requests
from bots import urls
import bots
import json
import pyrebase
import datetime as dt
endpoint = '/tito'
channel = 'Acceptance Test'
config = {
    "apiKey": "AIzaSyCxp8GD6IHlziwPRBRKPubXkMGvMA3tzUw",
    "authDomain": "hypechat-taller2.firebaseapp.com",
    "databaseURL": "https://hypechat-taller2.firebaseio.com/",
    "storageBucket": "projectId.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
class TestApi(unittest.TestCase):
    def assertEqualInDB(self,rv,expected):
        msgId = json.loads(rv.data.replace("'","\""))['name']
        msg = db.child(channel).child(msgId).get().val()['texto']
        db.child(channel).child(msgId).remove()
        self.assertEqual(msg, expected)

    def test_action_help(self):
        api = bots.create_app().test_client()
        body = {'message':'help',
                'metadata':{"orgId":123,
                            "firebaseToken":channel,
                            "channel":'canaleta',
                            "senderEmail":"user@email.com"
                            }}
        expected = 'Available commands: help, info, mute<n>, me'
        rv = api.post(endpoint,json=body)
        self.assertEqualInDB(rv,expected)

    def test_greet_new_user(self):
        api = bots.create_app().test_client()
        body = {'message':'greet user@email.com',
                'metadata':{'orgId':123,
                            'firebaseToken':channel,
                            'channel':'canaleta',
                            'senderEmail':"user@email.com"
                }
        }
        expected = "Bienvenido {} al canal {}".format("user@email.com",'canaleta')
        rv = api.post(endpoint,json=body)
        self.assertEqualInDB(rv,expected)

if __name__=='__main__':
    unittest.main()

