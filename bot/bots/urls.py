host = "https://secure-plateau-18239.herokuapp.com"
urls = {
    "hypechat":{
        'userInfo': host+"/profile/{email}",
        'channelInfo':host+'/channel/{token}/{orgId}/{channelName}'
    }
}
