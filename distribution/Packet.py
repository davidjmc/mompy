from distribution.PacketBody import PacketBody
from distribution.PacketHeader import PacketHeader


class Packet:

    def __init__(self, packetheader, parameters, message):
        self.packetHeader = PacketHeader(packetheader)
        self.packetBody = PacketBody(parameters, message)