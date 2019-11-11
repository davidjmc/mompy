import socket
import sys

from messages.MessageSAM import MessageSAM
from messages.Invocation import Invocation
from common.Marshaller import marshall

active_consumer = {}
c = None
host = None


def notify_subscribers(subscribers, msg_tobe_notified):
    global c, host
    if subscribers is not None:
        for subscriber in subscribers:
            ip, port = subscriber
            # print(ip)
            # print(port)
            # print(msg_tobe_notified)

            c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = (str(ip), int(port))

        try:
            # Connect the socket to the port where the server is listening
            # print('Connecting to {} port {}'.format(*host))
            c.connect(host)

            # Send data
            data = marshall(msg_tobe_notified)
            c.sendall(data)
            c.close()


        except:
            print("Connection error")
            sys.exit()

        #return _r.response


def i_notify(msg: MessageSAM):
    inv: Invocation = msg.payload
    subs = []

    op = inv.Op
    if op == "Notify":
        args = inv.Args
        subs = args[0]
        msg = args[1]
        notify_subscribers(subs, msg)
    else:
        print("NotificationConsumer:: Operation " + inv.Op + "is not implemented by NotificationConsumer")
