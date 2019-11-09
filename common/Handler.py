import socket
import sys
import traceback

from threading import Thread
from common.Marshaller import unmarshall


def handler_thread(self, conn, ip, port):
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


class Handler:
    # Create a new socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    message: None
    connection: None

    def __init__(self, ip, port):
        self._ip = ip
        self._port = port

    def set_result(self, msg):
        self.message = msg

    def get_result(self):
        return self.message

    def start_handler(self):

        # Create an endpoint
        addr = (self._ip, self._port)
        # print('Starting up on {} port {}'.format(*addr))

        try:
            # Binds the socket object to address composed of a host and port number
            self.server.bind(addr)

        except:

            print("Bind failed. Error : " + str(sys.exc_info()))
            sys.exit()

        # Listen for accepting connections
        self.server.listen()
        print("Socket now listening")

        while True:

            connection, cli = self.server.accept()

            try:
                ip, port = str(cli[0]), str(cli[1])
                Thread(target=handler_thread, args=(self, connection, ip, port)).start()

            except:

                print("Thread did not start.")
                traceback.print_exc()
