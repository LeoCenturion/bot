from . import bot
from flask import request
import datetime as dt
import requests
from . import urls
import pyrebase
import datetime as dt
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
            'me'  : lambda msg: self.getUserInfo(msg['parameters'][0]),
            'info': lambda msg: self.getChannelInfo(msg['metadata']['orgId'],
                                                    msg['metadata']['channel'],
                                                    msg['metadata']['firebaseToken']),
            'greet':lambda msg: self.greetNewMember(msg['metadata']['channel'],
                                                  msg['metadata']['senderEmail'],
                                                  msg['metadata']['firebaseToken']
            )
        })

    def post(self):
 #       if(self.isMuted()):
  #          return
        message = request.get_json()

        message = self._parseMessage(message)
        return self._handleMessage(message)

    def help(self,token):
        helpMessage = 'Available commands: help, info, mute<n>, me'
        return self.sendToFirebase(helpMessage,token )

    def mute(self,n):
#        url = str(urls)
        self.wakeUpTime = dt.datetime.now() + dt.timedelta(int(n))

    def isMuted(self):
        return (self.wakeUpTime>dt.datetime.now())

    def getUserInfo(self,userEmail):
        url = str(urls.urls['hypechat']['userInfo']).format(email=userEmail )
        response = requests.get(url)
        return self.sendToFirebase()

    def getChannelInfo(self,orgId,channelName,token):
        url = str(urls.urls['hypechat']['channelInfo'].format(orgId=orgId, channelName=channelName,token=token))
        response = requests.get(url)
        return response.json()

    def greetNewMember(self,channelName,email,token):
        message = "Bienvenido {} al canal {}".format(email,channelName)
        return self.sendToFirebase(message,token)

    def sendToFirebase(self,message, token):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        data = {"email" : "",
                "hora" : str(dt.datetime.now()),
                "nickname" : "titoElBot",
                "texto" : message,
                "url_foto_perfil" : ""
        }
        return db.child(token).push(data)
