from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("logbook", "0002_imports_staged"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="logentry",
            index=models.Index(fields=["qso_date", "time_on"], name="qso_datetime_idx"),
        ),
        migrations.AddIndex(
            model_name="logentry",
            index=models.Index(fields=["band"], name="qso_band_idx"),
        ),
        migrations.AddIndex(
            model_name="logentry",
            index=models.Index(fields=["mode"], name="qso_mode_idx"),
        ),
        migrations.AddIndex(
            model_name="logentry",
            index=models.Index(fields=["gridsquare"], name="qso_grid_idx"),
        ),
        migrations.AddIndex(
            model_name="logentry",
            index=models.Index(fields=["dxcc"], name="qso_dxcc_idx"),
        ),
    ]

