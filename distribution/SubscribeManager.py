from distribution.SubscriberRecord import SubscriberRecord
from messages.MessageSAM import MessageSAM
from messages.Invocation import Invocation
from common.QueueTermination import QueueTermination

subscribe_sm = {}


def subscribe(topic, ip, port):
    r = True

    if topic in subscribe_sm.keys():
        subscribers = subscribe_sm[topic]
        new_subs = (ip, port)

        if new_subs in subscribers:
            pass
        else:
            subscribers.append(new_subs)
            subscribe_sm[topic] = subscribers

    else:
        subs = (ip, port)
        subscribe_sm[topic] = [subs]

    print(subscribe_sm[topic])
    return r


def getsubscribers():
    return subscribe_sm


def i_posinvp(msg: MessageSAM):
    inv: Invocation = msg.payload

    op = inv.Op
    if op == "Subscribe":

        _args = inv.Args
        _topic = _args[0]
        _ip = _args[1]
        _port = int(_args[2])

        # print("Topic -> " + _topic)
        # print("ip -> " + _ip)
        # print("port -> " + str(_port))

        _r = subscribe(_topic, _ip, _port)
        #_ter = QueueTermination(_r)

        inv.Op = "GetSubscribers"
        msg.payload = inv
        return msg, True

    elif op == "Unsubscribe":
        print("SubscribeManager.Unsubscribe")
    elif op == "GetSubscribers":
        subs = getsubscribers()
        return msg, subs
    else:
        print("SubscribeManager:: Operation " + inv.Op + " is not implemented by Subscribe Manager")
