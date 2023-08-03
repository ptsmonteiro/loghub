import unittest
import n1mm

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

adif = """
<band:3>40m
<call:5>F4HDC
<country:6>France
<freq:5>7.130
<mode:3>SSB
<my_sig:4>POTA
<name:15>Michel Collorec
<operator:7>F4JAW
<qso_date:8>20230707
<qso_date_off:8>20230707
<qth:8>CRAYSSAC
<rst_rcvd:2>45
<rst_sent:2>59
<time_on:6>101015
<eor>
"""

class TestN1MM(unittest.TestCase):

    def test_to_adif_field_with_empty_data(self):
        self.assertEqual(n1mm.to_adif_field('test', ''), '', "Should return empty")

    def test_to_adif_field(self):
        self.assertEqual(n1mm.to_adif_field('freq', '28.074'), "<freq:6>28.074\n")

    def test_freq_to_adif(self):
        self.assertEqual(n1mm.freq_to_adif(2807535), '28.07535')

    def test_contact_to_adif(self):
        adif = n1mm.contact_to_adif(message)
        self.assertIn("<qso_date:8>20230630\n", adif)
        self.assertIn("<time_on:6>180030\n", adif)
        self.assertIn("28.07535\n", adif)

if __name__ == '__main__':
    unittest.main()
