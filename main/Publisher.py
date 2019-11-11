import time

from distribution import QueueManagerProxy


class Publisher(object):

    @staticmethod
    def main():
        idx: int = 0

        while True:
            msg = "msg [" + str(idx) + "]"
            r = QueueManagerProxy.pusblish("queue1", msg)
            print("Producer: " + msg + " " + str(r))
            time.sleep(4)
            idx = idx + 1


if __name__ == '__main__':
    Publisher().main()
