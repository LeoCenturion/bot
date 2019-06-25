import unittest
import sys
sys.path.append('../')
import bots
import mock
import requests
from bots import urls
import bots
endpoint = '/tito'
class TestApi(unittest.TestCase):
    def test_action_help(self):
        api = bots.create_app().test_client()
        body = {'message':'help',
                'metadata':''}
        expected = 'Available commands: help, info, mute<n>, me'
        rv = api.post(endpoint,data=body)
        self.assertEqual(rv.data.rstrip("\n").replace('"',''), expected)


if __name__=='__main__':
    unittest.main()

