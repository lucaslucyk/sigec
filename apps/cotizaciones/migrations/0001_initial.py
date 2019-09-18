# Generated by Django 2.2.4 on 2019-09-05 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('data', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('imagen', models.ImageField(blank=True, help_text='Para usarla en el producto si no tiene imagen.', null=True, upload_to='imgs_grupo/', verbose_name='Imagen')),
            ],
            options={
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('costo', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
                ('imagen', models.ImageField(blank=True, help_text='Si no se carga, usa la imagen del grupo.', null=True, upload_to='imgs_producto/', verbose_name='Imagen')),
                ('descripcion', models.CharField(max_length=255, unique=True)),
                ('categoria', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Categoria')),
                ('grupo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cotizaciones.Grupo')),
                ('software_compatible', models.ManyToManyField(blank=True, to='data.Software')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Oferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asunto', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha', models.DateField(auto_now_add=True, null=True)),
                ('tasa_cambio', models.DecimalField(decimal_places=2, default=1.0, max_digits=10)),
                ('oc_autorizacion', models.FileField(blank=True, help_text='Se agrega al obtener la OC o aprobación del cliente.', null=True, upload_to='oc_autoriz/ofertas/', verbose_name='OC - Aprobacion')),
                ('facturado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.Cliente')),
                ('moneda', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='data.Moneda')),
                ('usuario', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Oferta',
                'verbose_name_plural': 'Ofertas',
            },
        ),
        migrations.CreateModel(
            name='LineaOferta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('costo_custom', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('oferta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cotizaciones.Oferta')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotizaciones.Producto')),
            ],
            options={
                'verbose_name': 'Producto ofertado',
                'verbose_name_plural': 'Productos ofertados',
            },
        ),
    ]