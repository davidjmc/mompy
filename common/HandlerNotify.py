import socket
import sys
import traceback
from threading import Thread
from typing import Type

from common.Marshaller import unmarshall
from messages.MIOP import MIOP

# class HandlerNotify:

# IP and Port
h = "127.0.0.1"
p = 64000
result: Type[str] = str

# Create a new socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

connection = None


# def __init__(self, ip, port):
#   self.ip = ip
#  self.port = port


def set_result(res):
    global result
    result = res


def handler_thread(conn, ip, port):
    global result
    is_active = True

    while is_active:
        data = conn.recv(1024)
        # print('Received {!r}'.format(data))
        # data_size = sys.getsizeof(data)

        if not data:
            break

        result = unmarshall(data)
        print("asdlkjjaslkflkasjflahlsfjklasjdlkjaslkjdfalsjfjaslkjdlkasjdlkjaskldjlasj")
        print(result)
        set_result(result)

    conn.close()


def start_handler(handler):
    global server, result
    # Create an endpoint
    # addr = (handler(0), handler(1))
    # print('Starting up on {} port {}'.format(*addr))

    try:
        # Binds the socket object to address composed of a host and port number
        server.bind(handler)

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

            msg = Thread(target=handler_thread, args=(connection, ip_client, port_client)).start()


            #while True:
             #   data = connection.recv(1024)
                # print('Received {!r}'.format(data))
                # data_size = sys.getsizeof(data)

              #  if not data:
               #     break

                # print('Sending data to the Queue Manager')
                #msg = unmarshall(data)
                #print("AQUIIIIIII")
                #print(msg)
                #set_results(msg)

            #connection.close()
            #return msg

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
            msg = get_results()

            return msg

        except:
            print("Thread did not start.")
            traceback.print_exc()


def get_results():
    return result


def start(self):
    pass


# def handler_thread(conn, ip, p):
#    print("Connected by " + ip + ":" + p)

#    is_active = True

#    while is_active:
#        data = conn.recv(1024)
# print('Received {!r}'.format(data))
# data_size = sys.getsizeof(data)

#        if not data:
#            break

# print('Sending data to the Queue Manager')
#        msg = unmarshall(data)
#        print(msg)
#        return msg

#    connection.close()

