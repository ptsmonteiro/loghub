import asyncio
import configparser

import n1mm
import clublog

config = None

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        n1mm_xml = data.decode()
        print('Received %s from %s' % (n1mm_xml, addr))

        adif = n1mm.contact_to_adif(n1mm_xml)
        clublog.realtime_api(
            config['clublog']['email'], 
            config['clublog']['password'],
            config['clublog']['callsign'], adif)

        #print('Send %s to %s' % (message, addr))
        #self.transport.sendto(data, addr)


async def main():

    config = configparser.ConfigParser()
    config.read('config.ini')

    print("Starting UDP server")

    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    # One protocol instance will be created to serve all
    # client requests.
    transport, protocol = await loop.create_datagram_endpoint(
        lambda: EchoServerProtocol(),
        local_addr=('127.0.0.1', 12060))

    try:
        await asyncio.sleep(3600)  # Serve for 1 hour.
    finally:
        transport.close()


asyncio.run(main())
