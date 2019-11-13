import socket

from distribution import QueueManagerProxy


def web_page():
    html = """<html>
                <head> 
                    <title>ESP Web Server</title> 
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <link rel="icon" href="data:,">
                    <style> 
                        html{
                            font-family: Helvetica; 
                            display:inline-block; 
                            margin: 0px auto; 
                            text-align: center;
                        }
                        h1{
                            color: #0F3376; 
                            padding: 2vh;
                        }
                        p{
                            font-size: 1.5rem;
                        }
                        .button{
                            display: inline-block; 
                            background-color: #e7bd3b; 
                            border: none; 
                            border-radius: 4px; 
                            color: white; 
                            padding: 16px 40px; 
                            text-decoration: none; 
                            font-size: 30px; 
                            margin: 2px; 
                            cursor: pointer;
                            }
                        .button2{
                            background-color: #4286f4;
                            }
                    </style>
                </head>
                <body>
                    <h1>LED Action Web Server</h1> 
                    <table align="center" cellspacing=5 cellpadding=50>
                        <tr>
                            <td align="center" colspan="4">
                                <p><strong> RED LED </strong></p>
                                <p><a href="/?led=red_on"><button class="button">ON</button></a></p>
                                <p><a href="/?led=red_off"><button class="button button2">OFF</button></a></p>
                            </td>
                            <td align="center">
                                <p><strong> YELLOW LED</strong></p>
                                <p><a href="/?led=yellow_on"><button class="button">ON</button></a></p>
                                <p><a href="/?led=yellow_off"><button class="button button2">OFF</button></a></p>
                            </td>
                            <td align="center">
                                <p><strong> GREEN LED </strong></p>
                                <p><a href="/?led=green_on"><button class="button">ON</button></a></p>
                                <p><a href="/?led=green_off"><button class="button button2">OFF</button></a></p>
                            <td>
                        </tr>
                    </table>
                    </body>
                    </html>"""
    return html


web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
web.bind(('', 80))
web.listen()


def send_action(action):
    ddr = ('192.168.1.9', 10000)

    while True:
        c = socket.socket()
        c.connect(ddr)
        print(action)
        c.sendall(bytes(action, "utf-8"))
        break


while True:
    conn, addr = web.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    # led_on = request.find('/?led=on')
    # led_off = request.find('/?led=off')
    if "red_on" in request:
        QueueManagerProxy.pusblish("queue1", "red on")
    elif "red_off" in request:
        QueueManagerProxy.pusblish("queue1", "red off")
    elif "yellow_on" in request:
        QueueManagerProxy.pusblish("queue1", "yellow on")
    elif "yellow_off" in request:
        QueueManagerProxy.pusblish("queue1", "yellow off")
    elif "green_on" in request:
        QueueManagerProxy.pusblish("queue1", "green on")
    elif "green_off" in request:
        QueueManagerProxy.pusblish("queue1", "green off")
    response = web_page()
    # conn.send('HTTP/1.1 200 OK\n')
    # conn.send('Content-Type: text/html\n')
    # conn.send('Connection: close\n\n')
    conn.sendall(response.encode())
    conn.close()
