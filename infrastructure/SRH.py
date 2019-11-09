import socket
import sys
import traceback

from threading import Thread
from common.Marshaller import unmarshall, marshall
from common.QueueTermination import QueueTermination
from distribution import QueueInvoker
from messages.MIOP import MIOP
from messages.MessageSAM import MessageSAM

# print("I'm SRH!")

# IP and Port
host = "127.0.0.1"
port = 65000

# Create a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

connection = None


# print("Socket Created!")


def connection_thread(conn, ip, p):
    # print("Connected by " + ip + ":" + p)

    is_active = True

    while is_active:
        data = conn.recv(1024)
        # print('Received {!r}'.format(data))
        # data_size = sys.getsizeof(data)

        if not data:
            break

        # print('Sending data to the Queue Manager')
        msg: MIOP = unmarshall(data)
        _r = QueueInvoker.i_posinvp(msg)

        if _r is not None:
            _ter = QueueTermination(_r)
            msg = MessageSAM(_ter)
            data = marshall(msg)
            conn.sendall(data)

    conn.close()


def i_preinvr():
    global server
    # Create an endpoint
    addr = (host, port)
    # print('Starting up on {} port {}'.format(*addr))

    try:
        # Binds the socket object to address composed of a host and port number
        server.bind(addr)

    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()

    # Listen for accepting connections
    server.listen()
    print("Socket now listening")

    while True:

        # Accepts incoming connections and returns a tuple (conn, address)
        # print('Waiting for a New Connection: ')
        global connection
        connection, client_address = server.accept()

        try:
            ip_client, port_client = str(client_address[0]), str(client_address[1])

            Thread(target=connection_thread, args=(connection, ip_client, port_client)).start()

            # Receive the data in small chunks
            # while True:
            # data = connection.recv(1024)
            # print('Received {!r}'.format(data))

            # if data:
            #   print('Sending data to the Queue Manager')
            #  msg: MIOP = unmarshall(data)
            # invoker_receive(msg)

            # else:
            #   print('no data from', client_address)
            #  break

        except:
            print("Thread did not start.")
            traceback.print_exc()

    # server.close()


def i_posterr(msg: MessageSAM):
    pass
    # _miop: MIOP = msg.payload

    # header = _miop.header
    # body: MIOPBody = _miop.body

    # reply_header: ReplyHeader = body.requestHeader
    # reply_body: ReplyBody = body.requestBody

    # print("SRH:: ")
    # print(header.magic)
    # print(reply_header.status)
    # print(reply_body.reply)
