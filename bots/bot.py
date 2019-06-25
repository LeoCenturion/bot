from flask_restful import Resource

class Bot(Resource):
    def __init__(self):
        self.handlers = {}

    def _handleMessage(self,message): #
        handler = self.handlers[message['action']]
        result = handler(message)
        return result

    def _parseMessage(self,m):
        args = {}
        s = m['message'].split(" ")
        args['action'] = s.pop(0)
        args['parameters'] = []
        for parameter in s:
            args['parameters'].append(parameter)
        args['metadata']=m['metadata']
        return args


