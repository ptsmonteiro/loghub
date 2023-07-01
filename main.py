import asyncio
import xml.etree.ElementTree as ET

message = """<?xml version="1.0" encoding="utf-8"?>
<contactinfo>
        <app>N1MM</app>
        <contestname>DX</contestname>
        <contestnr>0</contestnr>
        <timestamp>2023-06-30 18:00:30</timestamp>
        <mycall>F4JAW</mycall>
        <band>28</band>
        <rxfreq>2807535</rxfreq>
        <txfreq>2807535</txfreq>
        <operator>F4JAW</operator>
        <mode>FT8</mode>
        <call>EA5EB</call>
        <countryprefix>EA</countryprefix>
        <wpxprefix>EA5</wpxprefix>
        <stationprefix></stationprefix>
        <continent>EU</continent>
        <snt>-08</snt>
        <sntnr>0</sntnr>
        <rcv>-11</rcv>
        <rcvnr>0</rcvnr>
        <gridsquare>IM99</gridsquare>
        <exchange1></exchange1>
        <section></section>
        <comment>Balcony Outback 2000</comment>
        <qth></qth>
        <name></name>
        <power></power>
        <misctext></misctext>
        <zone>0</zone>
        <prec></prec>
        <ck>0</ck>
        <ismultiplier1>0</ismultiplier1>
        <ismultiplier2>0</ismultiplier2>
        <ismultiplier3>0</ismultiplier3>
        <points>1</points>
        <radionr>0</radionr>
        <run1run2>1</run1run2>
        <RoverLocation></RoverLocation>
        <RadioInterfaced>0</RadioInterfaced>
        <NetworkedCompNr>0</NetworkedCompNr>
        <IsOriginal>True</IsOriginal>
        <NetBiosName>8700K</NetBiosName>
        <IsRunQSO>0</IsRunQSO>
        <StationName>8700K</StationName>
        <ID>cc186cb34185419db60f4388391bf508</ID>
        <IsClaimedQso>1</IsClaimedQso>
        <oldtimestamp>2023-06-30 18:00:30</oldtimestamp>
        <oldcall>EA5EB</oldcall>
</contactinfo>"""

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %s from %s' % (message, addr))
        print('Send %s to %s' % (message, addr))
        #self.transport.sendto(data, addr)


async def main():
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
