from infrastructure import CRH
from messages.MIOP import MIOP
from messages.MIOPBody import MIOPBody
from messages.MIOPHeader import MIOPHeader
from messages.MessageSAM import MessageSAM
from messages.RequestBody import RequestBody
from messages.RequestHeader import RequestHeader
from messages.ToCRH import ToCRH


# print("I'm Requestor!")


def i_posinvp(msg: MessageSAM):
    invocation = msg.payload

    request_header = RequestHeader(invocation.Op)
    request_body = RequestBody(invocation.Args)

    miop_header = MIOPHeader("MIOP")
    miop_body = MIOPBody(request_header, request_body)
    miop = MIOP(miop_header, miop_body)
    toCRH = ToCRH(invocation.Host, invocation.Port, miop)

    # print(invocation.Host)
    # print(invocation.Port)
    # print(invocation.Op)
    # print(invocation.Args)

    msg.payload = toCRH
    _r = CRH.i_posinvp(msg)

    return _r


def i_posterr():
    pass
    # r = CRH.i_preterp()

    # miop_body = r.payload
