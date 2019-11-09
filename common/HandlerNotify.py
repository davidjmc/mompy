import socket
import sys
import traceback
from threading import Thread
from typing import Type

from common.Marshaller import unmarshall
from messages.MIOP import MIOP


class HandlerNotify:
    pass
    '''
    result: Type[str] = str
    connection: None

    # Create a new socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    def set_result(self, res):
        global result
        result = res

    def handler_thread(self, conn, ip, port):
        global result
        is_active = True

        while is_active:
            data = conn.recv(1024)
            # print('Received {!r}'.format(data))
            # data_size = sys.getsizeof(data)

            if not data:
                break

            result = unmarshall(data)
            self.set_result(result)
            print(result)

        conn.close()

    def start_handler(self):
        global server, result
        # Create an endpoint
        addr = (self.ip, self.port)
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
        # global connection
        connection, client_address = server.accept()

        try:
            ip_client, port_client = str(client_address[0]), str(client_address[1])

            Thread(target=handler_thread, args=(connection, ip_client, port_client)).start()

        except:
            print("Thread did not start.")
            traceback.print_exc()
'''