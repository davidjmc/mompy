import time

from distribution import QueueManagerProxy


class Subscribe(object):

    @staticmethod
    def main():
        msg, r = QueueManagerProxy.subscribe("queue1")

        while True:
            # QueueManagerProxy.subscribe("queue1")
            print("Subscribe:: " + str(msg))
            # queueingproxy.consumer("queue1")
            time.sleep(4)


if __name__ == '__main__':
    Subscribe().main()
