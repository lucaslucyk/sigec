from django.db import models
from django.contrib.auth.models import User
from apps.data.models import Moneda
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.conf import settings
from apps.data.modules import functions

from django.db.models import Q

## news ##

class Plan(models.Model):
    """ for 36, 48 and more future plans """

    meses = models.PositiveIntegerField('Meses de financiación', default=0, unique=True)

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Planes"

    def __str__(self):
        return f'{self.meses} meses'

    
class TipoVenta(models.Model):
    """ for end user, partner and future sell types """

    nombre = models.CharField(max_length=50, null=True, blank=True, unique=True)
    moneda = models.ForeignKey(Moneda, blank=True, null=True, on_delete=models.SET_NULL)
    directa = models.BooleanField(default=False,  help_text='Marcar si el tipo es directa.')

    class Meta:
        verbose_name = "Tipo de venta"
        verbose_name_plural = "Tipos de venta"

    def __str__(self):
        return f'{self.nombre}'


# class Hardware(models.Model):
#     """ for propio, terceros and future hardware providers """

#     proveedor = models.CharField(max_length=50, null=True, blank=True, unique=True)

#     class Meta:
#         verbose_name = "Hardware"
#         verbose_name_plural = "Hardwares"

#     def __str__(self):
#         return f'{self.proveedor}'


class EscalaPrecio(models.Model):
    """ for generate offer prices """

    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.CASCADE)
    tipos_de_venta = models.ManyToManyField(TipoVenta, blank=True)
    # hardware = models.ForeignKey(Hardware, blank=True, null=True, on_delete=models.CASCADE)

    precio_base = models.DecimalField("Precio base", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='"b" en f(x) = mx + b')
    
    minimo = models.PositiveIntegerField("Cantidad mínima", default=0, unique=False, help_text="Mínimo en tipo de venta y plan.")
    alcance = models.PositiveIntegerField("Cantidad máxima", default=0, unique=False) 
    
    tp_unidad = models.DecimalField("TP Unidad", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='"m" en f(x) = mx + b')

    descuento_terceros = models.DecimalField(default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Descuento sin el signo %. Ej. 135,5 (%)')

    class Meta:
        verbose_name = "Escala de Precio"
        verbose_name_plural = "Escalas de Precios"

    #@property
    def display_tdv(self):
        return ', '.join([str(tdv.nombre) for tdv in self.tipos_de_venta.all()])

    display_tdv.short_description = "Tipos de venta"

    def __str__(self):
        return f'f(x) = {self.tp_unidad}x + {self.precio_base}'

class Oferta(models.Model):
    """ for get all data """

    usuario = models.ForeignKey(User, default=1, null=True, 
        on_delete=models.SET_DEFAULT, related_name='usuario')
    fecha = models.DateField(auto_now_add=True, null=True)

    tipo_venta = models.ForeignKey(TipoVenta, blank=True, null=True, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, blank=True, null=True, on_delete=models.CASCADE)
    # hardware = models.ForeignKey(Hardware, blank=True, null=True, on_delete=models.CASCADE)

    empleados = models.PositiveIntegerField("Empleados", default=50, 
        validators=[MinValueValidator(50), MaxValueValidator(2000),],
        help_text='Cantidad de empleados. Indicar un valor entre 1 y 2000.'
    )

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"

    def __str__(self):
        return f'Oferta por {self.empleados} empleados'

    @property
    def moneda(self):
        return self.tipo_venta.moneda.codigo

    @property
    def offer_scale(self):
        """ returns all the scales for this cathegory. <QuerySet []> if not exists """
        
        _escalas = EscalaPrecio.objects.filter(
            plan=self.plan,
            #hardware=self.hardware,
            tipos_de_venta__in=[self.tipo_venta],

            alcance__gte = self.empleados,
            minimo__lte = self.empleados,
        ).order_by('alcance')

        return _escalas.first() if _escalas else _escalas

    @property
    def pvs_mensual(self):
        """ returns the suggested retail price to the end user """

        _escala = self.offer_scale
        if not _escala:
            return 0

        return round(_escala.precio_base + self.empleados * _escala.tp_unidad, 2)

    @property
    def pvs_total(self):
        return round(self.pvs_mensual * int(self.plan.meses), 2)
    

    @property
    def pv_mensual(self):
        """ for SPEC """

        if self.tipo_venta.directa:
            return self.pvs_mensual

        _escala = self.offer_scale
        if not _escala:
            return 0

        _desc = _escala.descuento_terceros
        if not _desc:
            return self.pvs_mensual

        return functions.porcentual(self.pvs_mensual, _desc, decremento=True)

    @property
    def pv_total(self):
        """ for SPEC """
        return round(self.pv_mensual * int(self.plan.meses), 2)

    @property
    def pv_capita(self):
        """ mensual for SPEC """
        return round(self.pv_mensual / self.empleados, 2)
    
    @property
    def costo_capita(self):
        return functions.porcentual(self.pv_capita, settings.PORCENTAJE_COSTO)

    @property
    def costo_mes(self):
        return functions.porcentual(self.pv_mensual, settings.PORCENTAJE_COSTO)

    @property
    def costo_total(self):
        return functions.porcentual(self.pv_total, settings.PORCENTAJE_COSTO)
    
    @property
    def margen_bruto(self):
        return round(float(self.pv_total) - self.costo_total, 2)
    
## news ##
