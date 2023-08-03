import xml.etree.ElementTree as ET
import datetime

def to_adif_field(adif_field, data):
    if data is None or len(data) <= 0:
        return ''
    
    adif = "<%s:%d>%s\n" % (adif_field, len(data), data)
    return adif

def xml_to_adif_field(xml_object, xml_field, adif_field, data = None):
    if data is None: 
        data = xml_object.find(xml_field).text

    return to_adif_field(adif_field, data)

def freq_to_adif(n1mmFreq):
    mhz = int(n1mmFreq) / 100000
    return str(mhz)

def contact_to_adif(message):
    adif = ''
    
    root = ET.fromstring(message)
    if root.find('app').text != 'N1MM':
        raise RuntimeError('Not an N1MM message')
    
    # date and time
    dt = datetime.datetime.fromisoformat(root.find('timestamp').text)
    adif += to_adif_field('qso_date', dt.date().strftime("%Y%m%d"))
    adif += to_adif_field('time_on', dt.time().strftime("%H%M%S"))

    adif += xml_to_adif_field(root, 'mycall', 'operator')
    adif += xml_to_adif_field(root, 'call', 'call')
    adif += xml_to_adif_field(root, 'mode', 'mode')

    # frequencies
    tx_freq = root.find('txfreq').text
    rx_freq = root.find('rxfreq').text
    adif += xml_to_adif_field(root, '', 'freq', freq_to_adif(tx_freq))
    if tx_freq != rx_freq :
        adif += xml_to_adif_field(root, '', 'freq_rx', freq_to_adif(rx_freq))

    adif += xml_to_adif_field(root, 'snt', 'rst_sent')
    adif += xml_to_adif_field(root, 'rcv', 'rst_rcvd')
    adif += xml_to_adif_field(root, 'power', 'rx_power')    
    adif += xml_to_adif_field(root, 'name', 'name')    
    adif += xml_to_adif_field(root, 'qth', 'qth')
    adif += xml_to_adif_field(root, 'comment', 'comment')
    adif += "\n<eor>\n"

    return adif