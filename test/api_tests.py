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
    def assertEqualInDB(self,rv,channel,expected):
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
        self.assertEqualInDB(rv,channel,expected)

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
        self.assertEqualInDB(rv,channel,expected)

    def test_user_info(self):
        api = bots.create_app().test_client()
        apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1ZDAxNzI0NzhjNmI4ZDAwMTcxODU0NDgifQ.tMtWn63rqytzXuLDtrT0wHj_84eGzJ_BmZ8rniNnU5w"
        body = {'message':'me',
                'metadata':{'orgId':123,
                            'firebaseToken':channel,
                            'channel':'canaleta',
                            'senderEmail':"test@1.com",
                            'apiToken': apiToken
                }
        }
        expected = "username {}, alias {}. Contact {}"\
                  .format("victoria","vicky","test@1.com")
        rv = api.post(endpoint,json=body)
        self.assertEqualInDB(rv,channel,expected)


    def test_channel_info(self):
        api = bots.create_app().test_client()
        channel = "5d0257e9b3a8033023c420e5"
        apiToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI1ZDAxNzI0NzhjNmI4ZDAwMTcxODU0NDgifQ.tMtWn63rqytzXuLDtrT0wHj_84eGzJ_BmZ8rniNnU5w"
        body = {'message':'info',
                'metadata':{'firebaseToken':channel,
                            'channel':'general',
                            'senderEmail':"test@1.com",
                            'apiToken': apiToken,
                            'orgId':"admin2019",
                }
        }
        url = str(urls.urls['hypechat']['channelInfo'].format(orgId="admin2019", channelName="general",token=apiToken))
        expected =  requests.get(url).content
        rv = api.post(endpoint,json=body)
        self.assertEqualInDB(rv,channel,expected)


if __name__=='__main__':
    unittest.main()

