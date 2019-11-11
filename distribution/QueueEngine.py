from distribution import QueueInvoker, QueueConsumer, SubscribeManager
from messages.MessageSAM import MessageSAM
from messages.MessageMOM import MessageMOM
from messages.Invocation import Invocation
from distribution.Header import Header
from common.QueueTermination import QueueTermination

# print("I'm QueueEngine!")

topics = {}
msgs = []
subscribers = {}


def publish(topic, msg_pub):
    if topic in topics.keys():
        messages = topics[topic]
        if len(messages) < 20:
            messages.append(msg_pub)
            #messages.insert(0, msg_pub)
            topics[topic] = messages
            r = True
        else:
            topics[topic] = messages
            r = False
    else:
        topics[topic] = [msg_pub]
        r = True

    # print(topics.keys())
    # print(len(topics[topic]))
    # print("publish " + str(r))
    return r


def filter_subscribers(topic_tobe_published):
    if topic_tobe_published in subscribers.keys():
        subs = subscribers[topic_tobe_published]
        return subs


def i_notify(topic_tobe_published, msg_tobe_notified):
    temp_subs = filter_subscribers(topic_tobe_published)
    args = [temp_subs, msg_tobe_notified]
    msg = MessageSAM(Invocation(None, None, "Notify", args))
    QueueConsumer.i_notify(msg)


def i_publish(invocation: Invocation):
    args = invocation.Args
    topic = args[0]
    mom: MessageMOM = args[1]

    mom_header = mom.header.destination
    mom_payload = mom.payload

    # print("topic -> " + topic)
    # print("mom.header -> " + mom_header)
    # print("mom.payload -> " + mom_payload)

    msg_pub = MessageMOM(Header(mom_header), mom_payload)

    topic_tobe_published = topic
    msg_tobe_notified = mom_payload

    r = publish(topic, msg_pub)

    # _ter = QueueTermination(r)

    # msg = MessageSAM(_ter)
    # QueueInvoker.i_posterr(msg)

    if r:
        i_notify(topic_tobe_published, msg_tobe_notified)

    return r


def consumer(topic):
    if topic in topics.keys():
        messages = topics[topic]
        if len(messages) == 0:
            _r = MessageMOM(Header(topic), "QUEUE EMPTY")
        else:
            _r = MessageMOM(Header(topic), messages)

            return _r


def i_consumer(inv: Invocation):
    _temp = inv.Args
    topic = _temp[0]

    _r = consumer(topic)


def i_getressubs(r: QueueTermination):
    ter = r.response


def i_posinvp(msg: MessageSAM):
    invocation = msg.payload
    global Op

    Op = invocation.Op
    if Op == "Subscribe":
        msg, _r = SubscribeManager.i_posinvp(msg)
        msg, subs = SubscribeManager.i_posinvp(msg)

        # print("-------------------------------------------------------------------------------------------------")
        # print(msg.payload)
        # print(subs)

        subscribers.update(subs)
        return _r
        #print(subscribers)

    elif Op == "Unsubscribe":
        print("imprime 1")
    elif Op == "GetSubscribers":
        print("imprime 2")
    elif Op == "Publish":
        _r = i_publish(invocation)
        return _r
    elif Op == "Consumer":
        i_consumer(invocation)
    else:
        print("QueueEngine:: Operation " + invocation.Op + " is not implemented by Engine")

    # print("I'm QueueEngine Invocation!")
    # print(invocation.Op)
