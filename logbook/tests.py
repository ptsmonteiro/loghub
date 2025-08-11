from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase

from .models import QSO, Upload


ADIF_SAMPLE = (
    "<CALL:3>ABC<QSO_DATE:8>20240101<TIME_ON:4>1234<FREQ:6>14.074<MODE:3>FT8<EOR>"
)


class UploadTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_requires_station_callsign(self):
        file = SimpleUploadedFile("log.adi", ADIF_SAMPLE.encode("utf-8"))
        response = self.client.post("/api/upload/", {"adif": file})
        self.assertEqual(response.status_code, 400)
        self.assertIn("station_callsign", response.json()["error"])

    def test_upload_with_callsign(self):
        file = SimpleUploadedFile("log.adi", ADIF_SAMPLE.encode("utf-8"))
        response = self.client.post(
            "/api/upload/", {"adif": file, "station_callsign": "MYCALL"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Upload.objects.count(), 1)
        self.assertEqual(QSO.objects.count(), 1)
        qso = QSO.objects.first()
        assert qso is not None
        self.assertEqual(qso.station_callsign, "MYCALL")
        self.assertEqual(qso.freq, Decimal("14.074"))

    def test_missing_required_fields(self):
        bad_adif = "<CALL:3>ABC<QSO_DATE:8>20240101<TIME_ON:4>1234<EOR>"
        file = SimpleUploadedFile("log.adi", bad_adif.encode("utf-8"))
        response = self.client.post(
            "/api/upload/", {"adif": file, "station_callsign": "MYCALL"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("required", response.json()["error"])
