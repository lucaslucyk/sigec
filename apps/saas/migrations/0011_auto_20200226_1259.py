# Generated by Django 2.2.10 on 2020-02-26 15:59

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saas', '0010_auto_20200226_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='margin',
            name='margin_spec',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Múltiplo del márgen', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('1.00'))], verbose_name='Margen Bruto SPEC'),
        ),
    ]
