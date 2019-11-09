import time

from distribution import QueueManagerProxy
from common import Handler


class Subscribe(object):

    @staticmethod
    def main():
        handler: Handler = QueueManagerProxy.subscribe("queue1")

        while True:
            # QueueManagerProxy.subscribe("queue1")
            print("Subscribe:: " + handler.get_result())
            # queueingproxy.consumer("queue1")
            time.sleep(4)


if __name__ == '__main__':
    Subscribe().main()
