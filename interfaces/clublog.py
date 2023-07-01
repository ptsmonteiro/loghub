import asyncio
import xml.etree.ElementTree as ET

async def send_qso(qso):
    payload = transform(qso)
    make_http_req_to_clublog(payload)
