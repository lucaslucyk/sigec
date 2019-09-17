# Generated by Django 2.2.4 on 2019-09-17 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_cliente_tipo_moneda'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='tipo_moneda',
        ),
        migrations.AddField(
            model_name='cliente',
            name='moneda',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Moneda'),
        ),
        migrations.AlterField(
            model_name='moneda',
            name='codigo',
            field=models.CharField(max_length=20),
        ),
    ]
