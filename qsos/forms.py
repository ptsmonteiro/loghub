from django import forms

from .models import QSO


class QSOForm(forms.ModelForm):
    class Meta:
        model = QSO
        fields = [
            "callsign",
            "qso_date",
            "time_on",
            "band",
            "mode",
            "submode",
            "rst_sent",
            "rst_rcvd",
            "freq",
            "band_rx",
            "freq_rx",
            "prop_mode",
            "sat_name",
            "station_callsign",
            "operator",
            "country",
            "gridsquare",
            "my_dxcc",
            "my_state",
            "my_cnty",
            "my_gridsquare",
            "my_vucc_grids",
            "my_cq_zone",
            "my_itu_zone",
            "comment",
        ]
        widgets = {
            "qso_date": forms.DateInput(attrs={"type": "date"}),
            "time_on": forms.TimeInput(attrs={"type": "time"}),
            "comment": forms.Textarea(attrs={"rows": 3}),
        }
