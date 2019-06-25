import unittest
import sys
sys.path.append('../')
import bots
import mock
import requests
from bots import urls
def mocked_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == urls.urls['hypechat']['userInfo'].format(email='juan@perez.com'):
        return MockResponse({"name": "juan",
                             "nickname": "perez",
                             "email":"juan@perez.com"}, 200)
    elif args[0] == urls.urls['hypechat']['channelInfo'].format(orgId='1234',channelName='canaleta',token="321"):
        return MockResponse({"name": "canaleta",
                             "members": ["perdo","juan","adriana"],
                             "messages":"128"},200)
    return MockResponse(None, 404)

class TestBot(unittest.TestCase):
    def test_message_parser(self):
        bot = bots.Bot()
        messageToParse = {'metadata':{'orgId':123,
                                      'token':321,
                                      'channel':'canaleta' },
                          'message':'a b c'}
        parsed = bot._parseMessage(messageToParse)
        expected = {'action':'a',
                    'parameters': ['b', 'c'],
                    'metadata':{'orgId':123,
                                'token':321,
                                'channel':'canaleta'
                    }
        }
        self.assertEqual(expected,parsed)


    def test_defaultHandling(self):
        bot = bots.Bot()

        bot.handlers = {
            'add': lambda args: int(args['parameters'][0]) + int(args['parameters'][1])
        }
        result = bot._handleMessage(bot._parseMessage({'message':'add 3 5','metadata':''  }))
        self.assertEqual(result,3+5)

class TestBotTito(unittest.TestCase):
    def test_help(self):
        tito = bots.BotTito()
        expectedResponse = 'Available commands: help, info, mute<n>, me'
        self.assertEqual(tito.help(),expectedResponse)

    def test_mute(self):
        tito = bots.BotTito()
        tito.mute(10)
        self.assertEqual(tito.isMuted(),True)

    def test_me(self):
        requests.get = mocked_get
        tito = bots.BotTito()
        response = tito.getUserInfo("juan@perez.com")
        self.assertEqual(response,{"name": "juan",
                                   "nickname": "perez",
                                   "email":"juan@perez.com"})
    def test_info(self):
        requests.get = mocked_get
        tito = bots.BotTito()
        response = tito.getChannelInfo("1234","canaleta","321")
        self.assertEqual(response,{"name": "canaleta",
                                   "members": ["perdo","juan","adriana"],
                                   "messages":"128"})
if __name__=='__main__':
    unittest.main()


