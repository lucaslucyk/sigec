# Generated by Django 2.2.4 on 2019-09-17 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='tipo_moneda',
            field=models.CharField(choices=[('U$D', 'Dólar billete'), ('U$DD', 'Dólar Divisa'), ('AR$', 'Pesos Argentinos')], default='U$D', max_length=1),
        ),
    ]