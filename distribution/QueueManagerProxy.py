from common import HandlerNotify
from distribution import Requestor
from messages.Invocation import Invocation
from messages.MessageSAM import MessageSAM
from messages.MessageMOM import MessageMOM
from distribution.Header import Header

handlers = {}


def pusblish(_p1, _p2):
    _temp = MessageMOM(Header("Header"), _p2)
    _args = [_p1, _temp]
    _req = MessageSAM(Invocation('127.0.0.1', 65000, "Publish", _args))

    # Requestor
    _r = Requestor.i_posinvp(_req)

    # _res = Requestor.i_posterr()
    # _payload = _res.payload
    # _reply = _payload["Reply"]
    # _r = _reply["R"]

    return _r


def consumer(_p1):
    _args = [_p1]
    _req = MessageSAM(Invocation('127.0.0.1', 65000, "Consumer", _args))

    # Requestor
    Requestor.i_posinvp(_req)


def subscribe(_p1):
    _p2 = '127.0.0.1'
    _p3 = 64000
    _args = [_p1, _p2, _p3]
    _req = MessageSAM(Invocation('127.0.0.1', 65000, "Subscribe", _args))

    # Requestor
    _r = Requestor.i_posinvp(_req)

    # _rep: MessageSAM = Requestor.i_posterr()

    # _payload = "Teste"
    # _reply = {"Reply", _payload}
    # _r = {"R"}

    # print(_r)

    if handlers.get(_p1) is None:
        # handlers[_p1] = HandlerNotify(_p2, _p3)
        handlers[_p1] = (_p2, _p3)

    # handler: HandlerNotify = handlers[_p1]
    msg = HandlerNotify.start_handler(handlers[_p1])
    # msg = handler.start_handler()

    return msg, _r
