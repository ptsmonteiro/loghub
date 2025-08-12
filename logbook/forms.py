from django import forms

from .models import LogEntry


class LogEntryForm(forms.ModelForm):
    extras = forms.JSONField(required=False, help_text="Optional: additional ADIF fields as a JSON object")

    class Meta:
        model = LogEntry
        fields = [
            "callsign",
            "qso_date",
            "time_on",
            "band",
            "mode",
            "submode",
            "rst_sent",
            "rst_rcvd",
            "qso_date_off",
            "time_off",
            "srx",
            "srx_string",
            "stx",
            "stx_string",
            "freq",
            "band_rx",
            "freq_rx",
            "prop_mode",
            "sat_name",
            "station_callsign",
            "operator",
            "country",
            "gridsquare",
            "name",
            "tx_pwr",
            "dxcc",
            "cq_zone",
            "itu_zone",
            "iota",
            "my_dxcc",
            "my_state",
            "my_cnty",
            "my_gridsquare",
            "my_vucc_grids",
            "my_cq_zone",
            "my_itu_zone",
            "my_name",
            "sig",
            "sig_info",
            "my_sig",
            "my_sig_info",
            "sota_ref",
            "my_sota_ref",
            "lotw_qsl_rcvd",
            "lotw_qsl_rcvd_date",
            "lotw_qsl_sent",
            "lotw_qsl_sent_date",
            "notes",
        ]
        widgets = {
            "qso_date": forms.DateInput(attrs={"type": "date"}),
            "time_on": forms.TimeInput(attrs={"type": "time"}),
            "qso_date_off": forms.DateInput(attrs={"type": "date"}),
            "time_off": forms.TimeInput(attrs={"type": "time"}),
            "lotw_qsl_rcvd_date": forms.DateInput(attrs={"type": "date"}),
            "lotw_qsl_sent_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inst = kwargs.get("instance") or getattr(self, "instance", None)
        if inst and getattr(inst, "extras", None):
            self.fields["extras"].initial = inst.extras.data

