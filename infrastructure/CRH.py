import socket
import sys

from common.Marshaller import marshall, unmarshall
from messages.MessageSAM import MessageSAM
from messages.MIOP import MIOP
from common.QueueTermination import QueueTermination

client = None


def i_posinvp(msg: MessageSAM):
    tocrh = msg.payload

    # Create a TCP/IP socket
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host = tocrh.host
    port = tocrh.port
    miop: MIOP = tocrh.miop

    addr = (str(host), int(port))
    # print(addr)

    try:
        # Connect the socket to the port where the server is listening
        # print('Connecting to {} port {}'.format(*addr))
        client.connect(addr)

        # Send data
        data = marshall(miop)
        client.sendall(data)

        _msg = client.recv(1024)
        d: MessageSAM = unmarshall(_msg)
        _r: QueueTermination = d.payload
        # print(d.payload)


    except:
        print("Connection error")
        sys.exit()

    return _r.response


def i_preterp():
    pass
