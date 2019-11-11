import time

from distribution import QueueManagerProxy
from common import Handler


class Subscribe(object):

    @staticmethod
    def main():
        QueueManagerProxy.subscribe("queue1")


if __name__ == '__main__':
    Subscribe().main()
