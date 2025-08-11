from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qsos", "0004_adif_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="qso",
            name="sig",
            field=models.CharField(blank=True, help_text="SIG (e.g., POTA/SOTA)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="sig_info",
            field=models.CharField(blank=True, help_text="SIG_INFO (e.g., park/summit ref)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_sig",
            field=models.CharField(blank=True, help_text="MY_SIG (e.g., POTA/SOTA)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_sig_info",
            field=models.CharField(blank=True, help_text="MY_SIG_INFO (e.g., park/summit ref)", max_length=32),
        ),
        migrations.AddField(
            model_name="qso",
            name="pota_ref",
            field=models.CharField(blank=True, help_text="POTA_REF (worked station)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_pota_ref",
            field=models.CharField(blank=True, help_text="MY_POTA_REF", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="sota_ref",
            field=models.CharField(blank=True, help_text="SOTA_REF (worked station)", max_length=16),
        ),
        migrations.AddField(
            model_name="qso",
            name="my_sota_ref",
            field=models.CharField(blank=True, help_text="MY_SOTA_REF", max_length=16),
        ),
    ]

