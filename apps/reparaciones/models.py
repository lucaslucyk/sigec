from django.db import models
from datetime import datetime
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.models import User
from apps.data.models import Cliente, Moneda
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal

class FamiliaRepuesto(models.Model):
    nombre = models.CharField(max_length=50, unique=True, null=False)
    descripcion = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "{}".format(self.nombre)

    class Meta:
        verbose_name = "Familia de repuesto"
        verbose_name_plural = "Familias de repuestos"

class Repuesto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    costo = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text='')
    familia = models.ForeignKey(FamiliaRepuesto, null=True, blank=False, on_delete=models.SET_NULL)

    def __str__(self):
        return "{} | {}".format(self.familia, self.nombre)

    class Meta:
        verbose_name = "Repuesto"
        verbose_name_plural = "Repuestos"

class Presupuesto(models.Model):
    usuario = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_DEFAULT)
    asunto = models.CharField(max_length=100)
    fecha = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, null=False, blank=False, default=1, on_delete=models.CASCADE)
    tasa_cambio = models.DecimalField(default=1.00, max_digits=10, decimal_places=2)
    oc_autorizacion = models.FileField("OC - Aprobacion", null=True, blank=True, upload_to='oc_autoriz/presupuestos/', help_text="Se agrega al obtener la OC o aprobación del cliente.")
    facturado = models.BooleanField(default=False)

    #filesPresup = FilerFileField(null=True, blank=True, related_name="files_presup", on_delete=models.SET_NULL)

    def costo_total(self):
        lineas = LineaPresupuesto.objects.filter(presupuesto=self.id)
        if (len(lineas) == 0):
            return 0
            
        valorFinal = 0
        for val in lineas:
            valorFinal += val.costo_custom * val.cantidad if val.costo_custom else val.repuesto.costo * val.cantidad * self.tasa_cambio
        return "%.02f"%(valorFinal)

    @mark_safe
    def fileLink(self):
        if self.oc_autorizacion:
            return mark_safe('<a href="{}" target="_blank">Enlace</a>'.format(self.oc_autorizacion.url))
        else:
            return mark_safe('<a href="''"></a>')

    @property
    def presup_aprobado(self):
        aprobado = True if self.oc_autorizacion else False
        return aprobado

    fileLink.allow_tags = True
    fileLink.short_description = "Link OC-Aprob"

    def user_names(self):
        return '{} {}'.format(self.usuario.first_name, self.usuario.last_name)
    user_names.short_description = "Usuario"
    

    def __str__(self):
        return "%s"%(self.asunto)

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"

class LineaPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, null=True, blank=False, on_delete=models.CASCADE)
    repuesto = models.ForeignKey(Repuesto, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    costo_custom = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text='')

    @mark_safe
    def presup_link(self):
        link = reverse("admin:reparaciones_presupuesto_change", args=[self.presupuesto.id]) #model name has to be lowercase
        return mark_safe('<a href="{}">{}</a>'.format(link, self.presupuesto.asunto))
    presup_link.allow_tags = True
    presup_link.short_description = "Presupuesto"

    def __str__(self):
        return "%s x %s"%(self.cantidad, self.repuesto)

    class Meta:
        verbose_name = 'Items en presupuesto'
        verbose_name_plural = 'Items en presupuestos'