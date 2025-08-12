from django import forms


class ADIFUploadForm(forms.Form):
    file = forms.FileField(allow_empty_file=False)
    station_callsign = forms.CharField(max_length=20, required=False, help_text="Optional station callsign context for this import")
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={"rows": 2}))

