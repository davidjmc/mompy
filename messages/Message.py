from distribution.MessageBody import MessageBody
from distribution.MessageHeader import MessageHeader


class Message:

    def __init__(self, header, body):
        self.header = MessageHeader(header)
        self.body = MessageBody(body)
