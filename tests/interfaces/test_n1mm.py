import unittest
import interfaces.n1mm as n1mm

class TestN1MM(unittest.TestCase):

    def test_message_to_qso(self):
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
        qso = n1mm.message_to_qso(message)
        self.assertIsNotNone(qso)
        self.assertEqual(len(qso.keys()), 47)
        self.assertEqual(qso['mycall'], 'F4JAW')

if __name__ == '__main__':
    unittest.main()
