from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qsos", "0003_alter_qso_gridsquare"),
    ]

    operations = [
        migrations.AddField(
            model_name="qso",
            name="qso_date_off",
            field=models.DateField(blank=True, help_text="QSO_DATE_OFF (optional)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="time_off",
            field=models.TimeField(blank=True, help_text="TIME_OFF (optional)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="srx",
            field=models.PositiveIntegerField(blank=True, help_text="SRX (optional)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="srx_string",
            field=models.CharField(blank=True, help_text="SRX_STRING (optional)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="stx",
            field=models.PositiveIntegerField(blank=True, help_text="STX (optional)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="stx_string",
            field=models.CharField(blank=True, help_text="STX_STRING (optional)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="name",
            field=models.CharField(blank=True, help_text="NAME (operator name of station worked)", max_length=64),
        ),
        migrations.AddField(
            model_name="qso",
            name="tx_pwr",
            field=models.DecimalField(blank=True, decimal_places=2, help_text="TX_PWR in watts", max_digits=6, null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="dxcc",
            field=models.PositiveIntegerField(blank=True, help_text="DXCC entity code (worked)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="cq_zone",
            field=models.PositiveIntegerField(blank=True, help_text="CQ zone (worked)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="itu_zone",
            field=models.PositiveIntegerField(blank=True, help_text="ITU zone (worked)", null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="iota",
            field=models.CharField(blank=True, help_text="IOTA reference (e.g., EU-005)", max_length=10),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_name",
            field=models.CharField(blank=True, help_text="MY_NAME (operator name)", max_length=64),
        ),
        migrations.AddField(
            model_name="qso",
            name="lotw_qsl_rcvd",
            field=models.CharField(blank=True, help_text="LOTW_QSL_RCVD (Y/N/R/I/V)", max_length=1),
        ),
        migrations.AddField(
            model_name="qso",
            name="lotw_qsl_rcvd_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="qso",
            name="lotw_qsl_sent",
            field=models.CharField(blank=True, help_text="LOTW_QSL_SENT (Y/N/R/I/V)", max_length=1),
        ),
        migrations.AddField(
            model_name="qso",
            name="lotw_qsl_sent_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]

