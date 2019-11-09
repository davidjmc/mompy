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


def connection_thread(conn, ip, p):
    is_active = True

    while is_active:
        data = conn.recv(1024)

        if not data:
            break

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
    print("SRH Socket now listening")

    while True:

        # Accepts incoming connections and returns a tuple (conn, address)
        # print('Waiting for a New Connection: ')
        global connection
        connection, client_address = server.accept()

        try:
            ip_client, port_client = str(client_address[0]), str(client_address[1])

            Thread(target=connection_thread, args=(connection, ip_client, port_client)).start()

        except:
            print("Thread did not start.")
            traceback.print_exc()


def i_posterr():
    pass

