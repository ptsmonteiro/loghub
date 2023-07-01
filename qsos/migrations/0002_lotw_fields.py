from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qsos", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="qso",
            name="callsign",
            field=models.CharField(db_index=True, help_text="CALL: Station worked", max_length=20),
        ),
        migrations.AlterField(
            model_name="qso",
            name="qso_date",
            field=models.DateField(help_text="QSO_DATE: UTC date contact established"),
        ),
        migrations.AlterField(
            model_name="qso",
            name="time_on",
            field=models.TimeField(help_text="TIME_ON: UTC time contact established"),
        ),
        migrations.AlterField(
            model_name="qso",
            name="band",
            field=models.CharField(blank=True, help_text="BAND, e.g., 20m (derived from FREQ if absent)", max_length=16),
        ),
        migrations.AlterField(
            model_name="qso",
            name="freq",
            field=models.DecimalField(blank=True, decimal_places=6, help_text="FREQ in MHz (e.g., 14.074)", max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="band_rx",
            field=models.CharField(blank=True, help_text="BAND_RX (optional)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="freq_rx",
            field=models.DecimalField(blank=True, decimal_places=6, help_text="FREQ_RX in MHz", max_digits=11, null=True),
        ),
        migrations.AlterField(
            model_name="qso",
            name="mode",
            field=models.CharField(help_text="MODE, e.g., SSB, FT8", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="submode",
            field=models.CharField(blank=True, help_text="SUBMODE (optional)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="prop_mode",
            field=models.CharField(blank=True, help_text="PROP_MODE; 'SAT' requires SAT_NAME", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="sat_name",
            field=models.CharField(blank=True, help_text="SAT_NAME if PROP_MODE is SAT", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="station_callsign",
            field=models.CharField(blank=True, help_text="STATION_CALLSIGN (optional)", max_length=20),
        ),
        migrations.AddField(
            model_name="qso",
            name="operator",
            field=models.CharField(blank=True, help_text="OPERATOR (optional; treated as station callsign if STATION_CALLSIGN absent)", max_length=20),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_dxcc",
            field=models.PositiveIntegerField(blank=True, help_text="MY_DXCC code", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_state",
            field=models.CharField(blank=True, help_text="MY_STATE (enumerated per ADIF)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_cnty",
            field=models.CharField(blank=True, help_text="MY_CNTY (enumerated per ADIF)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_gridsquare",
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_vucc_grids",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_cq_zone",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_itu_zone",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

