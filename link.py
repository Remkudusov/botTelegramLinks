class Link(object):

    def __init__(self, code, channelLink, notSub, sub):
        self.code = code
        self.channelLink = channelLink
        self.notSub = notSub
        self.sub = sub

    def changeChannelLink(self, channelLink):
        self.channelLink = channelLink

    def changeNotSub(self, notSub):
        self.notSub = notSub

    def changeSub(self, sub):
        self.sub = sub

    def getCode(self):
        return self.code

    def getChannelLink(self):
        return self.channelLink

    def getNotSub(self):
        return self.notSub

    def getSub(self):
        return self.sub

    def getInfo(self):
        answer = str(self.code) + ' ' + self.channelLink + ' ' + self.notSub + ' ' + self.sub
        return answer