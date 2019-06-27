from . import bot
from flask import request, g, config
import datetime as dt
import requests
from . import urls
import pyrebase
import datetime as dt
import json
import time as t
config = {
    "apiKey": "AIzaSyCxp8GD6IHlziwPRBRKPubXkMGvMA3tzUw",
    "authDomain": "hypechat-taller2.firebaseapp.com",
    "databaseURL": "https://hypechat-taller2.firebaseio.com/",
    "storageBucket": "projectId.appspot.com"
}

class BotTito(bot.Bot):
    def __init__(self):
        super(BotTito,self).__init__()
        self.handlers.update({
            'help': lambda msg: self.help(msg['metadata']['firebaseToken']),
            'mute': lambda msg: self.mute(msg['parameters'][0]),
            'me': lambda msg: self.getUserInfo(msg['metadata']['senderEmail'],
                                                 msg['metadata']['apiToken'],
                                                 msg['metadata']['firebaseToken']),
            'info': lambda msg: self.getChannelInfo(msg['metadata']['orgId'],
                                                    msg['metadata']['channel'],
                                                    msg['metadata']['apiToken'],
                                                    msg['metadata']['firebaseToken']),
            'greet':lambda msg: self.greetNewMember(msg['metadata']['channel'],
                                                  msg['metadata']['senderEmail'],
                                                    msg['metadata']['firebaseToken']),
        })

    def post(self):
        message = request.get_json()
        message = self._parseMessage(message)
        return self._handleMessage(message)
        try:
            return self._handleMessage(message)
        except KeyError :
            return "Command not found", 400


    def help(self,token):
        helpMessage = 'Available commands: help, info, mute<n>, me'
        return self.sendToFirebase(helpMessage,token ), 200

    def mute(self,n):
        botWakeUpTime = dt.datetime.now() + dt.timedelta(0,minutes=int(n))
        t.sleep(60*int(n))
        return 200

    def isMuted(self):
        print "isMuted"
        print botWakeUpTime
        return (botWakeUpTime > dt.datetime.now())

    def getUserInfo(self,userEmail, apiToken, firebaseToken):
        url = str(urls.urls['hypechat']['userInfo']).format(email=userEmail )
        response = requests.post(url,{'token':apiToken})
        data = json.loads(response.content)
        message = "username {}, alias {}. Contact {}"\
                  .format(data['name'],data['nickname'],data['email'])
        return self.sendToFirebase(message ,firebaseToken)

    def getChannelInfo(self,orgId,channelName,token, firebaseToken):
        url = str(urls.urls['hypechat']['channelInfo'].format(orgId=orgId, channelName=channelName,token=token))
        response = requests.get(url)
        message = response.content
        return self.sendToFirebase(message ,firebaseToken)

    def greetNewMember(self,channelName,email,token):
        message = "Bienvenido {} al canal {}".format(email,channelName)
        return self.sendToFirebase(message,token)

    def sendToFirebase(self,message, token):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        data = {"email" : "",
                "hora" : {".sv":"timestamp"},
                "nickname" : "titoElBot",
                "texto" : message,
                "url_foto_perfil" : ""
        }
        return db.child(token).push(data)
