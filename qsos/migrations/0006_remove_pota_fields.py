from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("qsos", "0005_pota_sota_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="qso",
            name="pota_ref",
        ),
        migrations.RemoveField(
            model_name="qso",
            name="my_pota_ref",
        ),
    ]

