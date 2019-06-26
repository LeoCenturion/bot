import unittest
import sys
sys.path.append('../')
import bots
from bots import botTito
from bots import bot
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

def mocked_sendToFirebase(message,token):
    s = message
    return s

class TestBot(unittest.TestCase):
    def test_message_parser(self):
        b = bot.Bot()
        messageToParse = {'metadata':{'orgId':123,
                                      'token':321,
                                      'channel':'canaleta' },
                          'message':'a b c'}
        parsed = b._parseMessage(messageToParse)
        expected = {'action':'a',
                    'parameters': ['b', 'c'],
                    'metadata':{'orgId':123,
                                'token':321,
                                'channel':'canaleta'
                    }
        }
        self.assertEqual(expected,parsed)


    def test_defaultHandling(self):
        b = bot.Bot()

        b.handlers = {
            'add': lambda args: int(args['parameters'][0]) + int(args['parameters'][1])
        }
        result = b._handleMessage(b._parseMessage({'message':'add 3 5','metadata':''  }))
        self.assertEqual(result,3+5)

class TestBotTito(unittest.TestCase):
    def test_help(self):
        tito = botTito.BotTito()
        expectedResponse = 'Available commands: help, info, mute<n>, me'
        self.assertEqual(tito.help(),expectedResponse)

    def test_mute(self):
        tito = botTito.BotTito()
        tito.mute(10)
        self.assertEqual(tito.isMuted(),True)

    def test_me(self):
        requests.get = mocked_get
        tito = botTito.BotTito()
        response = tito.getUserInfo("juan@perez.com")
        self.assertEqual(response,{"name": "juan",
                                   "nickname": "perez",
                                   "email":"juan@perez.com"})
    def test_info(self):
        requests.get = mocked_get
        tito = botTito.BotTito()
        response = tito.getChannelInfo("1234","canaleta","321")
        self.assertEqual(response,{"name": "canaleta",
                                   "members": ["perdo","juan","adriana"],
                                   "messages":"128"})
    def test_greet_member(self):
        requests.get = mocked_get
        tito = botTito.BotTito()
        tito.sendToFirebase = mocked_sendToFirebase
        response = tito.greetNewMember("canaleta","e@mail.com","token")
        expected = "Bienvenido {} al canal {}".format("e@mail.com","canaleta")
        self.assertEqual(response,expected)

if __name__=='__main__':
    unittest.main()


