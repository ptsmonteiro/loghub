import asyncio
import xml.etree.ElementTree as ET

# For the loop datagram endpoint
transport = None
protocol = None

# queue
message_queue = None

# N1MM XML message to generic LogHub QSO dict
def message_to_qso(message):
    qso = {}
    root = ET.fromstring(message)
    for i in root:
        qso[i.tag] = i.text
    return qso

class ServerHandler:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        qso = message_to_qso(message)
        message_queue.put_nowait(qso)

async def start(message_q):
    message_queue = message_q
    loop = asyncio.get_running_loop()
    print("Starting N1MM UDP server")
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: ServerHandler(),
        local_addr=('127.0.0.1', 12060))

async def stop():
    print("Stopping N1MM UDP server")
    transport.close()

#asyncio.run(start())
