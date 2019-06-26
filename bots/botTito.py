from . import bot
from flask import request
import datetime as dt
import requests
from . import urls
class BotTito(bot.Bot):
    def __init__(self):
        super(BotTito,self).__init__()
        self.handlers.update({
            'help': lambda msg: self.help(),
            'mute': lambda msg: self.mute(msg['parameters'][0]),
            'me'  : lambda msg: self.getUserInfo(msg['parameters'][0]),
            'info': lambda msg: self.getChannelInfo(msg['metadata']['orgId'],
                                                    msg['metadata']['channelInfo'],
                                                    msg['metadata']['token'])
        })

    def post(self):
 #       if(self.isMuted()):
  #          return
        message = request.form.to_dict()
        message = self._parseMessage(message)
        return self._handleMessage(message)

    def help(self):
        helpMessage = 'Available commands: help, info, mute<n>, me'
        return helpMessage

    def mute(self,n):
#        url = str(urls)
        self.wakeUpTime = dt.datetime.now() + dt.timedelta(int(n))

    def isMuted(self):
        return (self.wakeUpTime>dt.datetime.now())

    def getUserInfo(self,userEmail):
        url = str(urls.urls['hypechat']['userInfo']).format(email=userEmail )
        response = requests.get(url)
        return response.json()

    def getChannelInfo(self,orgId,channelName,token):
        url = str(urls.urls['hypechat']['channelInfo'].format(orgId=orgId, channelName=channelName,token=token))
        response = requests.get(url)
        return response.json()

