from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
#from django.template.defaultfilters import escape
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

User.add_to_class('body_font', models.CharField(max_length=50, unique=False, blank=True, null=True))

class Comercial(models.Model):
    nombre_apellido = models.CharField(max_length=50, unique=True)
    email = models.EmailField()

    def __str__(self):
        return "{}".format(self.nombre_apellido)
    class Meta:
        verbose_name = 'Comercial'
        verbose_name_plural = 'Comerciales'

class Contrato(models.Model):
    cobertura = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "%s"%(self.cobertura)

    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

class Moneda(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        #return ("%s"%(self.codigo))
        return f'{self.codigo} | {self.nombre}'

    class Meta:
        verbose_name = 'Moneda'
        verbose_name_plural = 'Monedas'

class Cliente(models.Model):
    id_sage = models.IntegerField(default=0, unique=True)
    nombre = models.CharField(max_length=80, unique=True)
    comercial = models.ForeignKey(Comercial, null=True, on_delete=models.SET_NULL)
    #sla = models.ForeignKey(Contrato, null=True, blank=True, on_delete=models.CASCADE)
    sla = models.ManyToManyField(Contrato, blank=True)
    vencimiento_sla = models.DateField()
    #tipo_moneda = models.ForeignKey("Tipo de moneda", Moneda, default=1, on_delete=models.SET_NULL)
    moneda = models.ForeignKey(Moneda, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def get_sla(self):
        return ", ".join([cl.cobertura for cl in self.sla.all()])
    get_sla.short_description = "Servicios"

    def mantenim_activo(self):
        return True if self.get_sla() and self.vencimiento_sla > datetime.now().date() else False
        #return activo

    mantenim_activo.boolean = True
    mantenim_activo.short_description = "Mantenimiento Activo?"

    def __str__(self):
        return "%s"%(self.nombre)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class Categoria(models.Model):
    
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return "{}".format(self.nombre)

class Software(models.Model):

    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)

    class Meta:
        verbose_name = "Software"
        verbose_name_plural = "Softwares"

    def __str__(self):
        return "{}".format(self.nombre)

