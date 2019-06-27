from . import bot
from flask import request, g, config
import datetime as dt
import requests
from . import urls, db
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
    def __init__(self,wakeUp):
        super(BotTito,self).__init__()
        self.wakeUp = wakeUp
        self.handlers.update({
            'help': lambda msg: self.help(msg['metadata']['firebaseToken']),
            'mute': lambda msg: self.mute(msg['parameters'][0], msg['metadata']['orgId'], msg['metadata']['channel']),
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
        if self.isMuted(message['metadata']['orgId'], message['metadata']['channel']):
            return 200
        return self._handleMessage(message)
        try:
            return self._handleMessage(message)
        except KeyError :
            return "Command not found", 400
        except:
            return "Server error", 500

    def help(self,token):
        helpMessage = 'Available commands: help, info, mute<n>, me'
        return self.sendToFirebase(helpMessage,token ), 200

    def mute(self,n,orgId,channelName,):
        botWakeUpTime = dt.datetime.now() + dt.timedelta(0,minutes=int(n))
        self.wakeUp[orgId][channelName] = botWakeUpTime
        return 200

    def isMuted(self,orgId,channelName):
        botWakeUpTime = self.wakeUp.get(orgId, {}).get(channelName, None)
        if not botWakeUpTime:
            botWakeUpTime = dt.datetime(1970,1,1)
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
        msg_count = self.countMessagesInChannel(firebaseToken)
        formated = self.formatChannelInfoMessage(message,msg_count)
        return self.sendToFirebase(formated ,firebaseToken)

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

    def countMessagesInChannel(self,token):
        firebase = pyrebase.initialize_app(config)
        db = firebase.database()
        count = len(db.child(token).get().key())
        return count

    def formatChannelInfoMessage(self,message, msg_count):
        d =json.loads( message.decode('string-escape').strip('"'))['channel']
        members = [str(m) for m in d['members']]

        return "Canal: {}, Integrantes: {}, Cantidad de Mensajes: {}, Descripcion: {},  Duenio: {}".format(d['name'], str(members),str(msg_count) ,d['description'], d['owner'])
