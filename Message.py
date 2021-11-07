import datetime

class Message:
    def __init__(self, user, word):
        self.user = user
        self.word = word
        self.count = 0
        self.timestamp = datetime.datetime.now()