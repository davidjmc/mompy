from distribution import QueueEngine
from infrastructure import SRH
from messages.Invocation import Invocation
from messages.MIOP import MIOP
from messages.MIOPHeader import MIOPHeader
from messages.MIOPBody import MIOPBody

# Here test
from messages.MessageSAM import MessageSAM
from messages.ReplyBody import ReplyBody
from messages.ReplyHeader import ReplyHeader

print("I'm QueueInvoker!")


def i_posinvp(miop: MIOP):
    header: MIOPHeader = miop.header
    body: MIOPBody = miop.body

    # print(header.magic)
    # print(body.requestHeader.operation)
    # print(body.requestBody.Args)

    # print(header.magic)
    sam = MessageSAM(Invocation(None, None, body.requestHeader.operation, body.requestBody.Args))

    _r = QueueEngine.i_posinvp(sam)

    return _r


def i_posterr(msg: MessageSAM):
    status = 1
    _ter = msg.payload

    if _ter is False:
        status = 0

    _reply_header = ReplyHeader(None, None, status)
    _reply_body = ReplyBody(_ter)
    _miop_header = MIOPHeader("MIOP")
    _miop_body = MIOPBody(_reply_header, _reply_body)
    _miop = MIOP(_miop_header, _miop_body)

    msg.payload = _miop

    SRH.i_posterr(msg)
