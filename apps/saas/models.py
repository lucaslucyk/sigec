from django.db import models
from django.contrib.auth.models import User
from apps.data.models import Cliente
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.conf import settings
from apps.data.modules import functions

from django.db.models import Q

# Create your models here.
class Margin(models.Model):

    financing = models.CharField("Financiación", max_length=2, choices=settings.FINANCING, blank=False, \
        default=settings.FINANCING[0][0], help_text="Meses de financiación.")
    hardware = models.CharField(max_length=1, choices=settings.HARDWARE, blank=False, \
        default=settings.HARDWARE[0][0], help_text="Utilizará hardware propio (SPEC) o de terceros?")
    tipo_venta = models.CharField("Tipo de venta", max_length=1, choices=settings.SELLER, blank=False, \
        default=settings.SELLER[0][0], help_text="Quién efectúa la venta?")

    margin_spec = models.DecimalField("Margen SPEC", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('1.00'))], help_text='Múltiplo del márgen')
    margin_integrador = models.DecimalField("Margen Integrador", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Múltiplo del márgen')
    margin_mayorista = models.DecimalField("Margen Mayorista", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Múltiplo del márgen')

    rebate = models.DecimalField("Rebate", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Múltiplo del rebate')
    
    def __str__(self):
        return f'{self.margin_spec} | {self.margin_integrador} | {self.margin_mayorista}'

    class Meta:
        verbose_name = "Margen & Rebate"
        verbose_name_plural = "Márgenes & Rebates"

class ModuloSaaS(models.Model):
    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)

    pricing_management = models.CharField("Pricing management", max_length=2, choices=settings.PRICING_MANAGEMENT, blank=False, \
        default=settings.PRICING_MANAGEMENT[0][0], help_text="Cómo se maneja el pricing del módulo?")

    @property
    def is_costo_fijo(self):
        return True if self.pricing_management == 'vf' else False

    @property
    def is_range_price(self):
        return True if self.pricing_management == 'rp' else False

    @property
    def is_var_cantidad(self):
        return True if self.pricing_management == 'pu' else False
    
    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Módulo SaaS"
        verbose_name_plural = "Módulos SaaS"

class EscalaTransferPrice(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    modulo = models.ForeignKey(ModuloSaaS, null=True, blank=True, on_delete=models.CASCADE)

    precio_base = models.DecimalField("Precio base", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Máximo de escala anterior (si existe).')
    
    alcance = models.PositiveIntegerField("Cantidad máxima", default=0, unique=False)  
    #Modificar para que valide Unique dentro del modulo
    
    tp_unidad = models.DecimalField("TP Unidad", default=0, max_digits=10, decimal_places=2, \
        validators=[MinValueValidator(Decimal('0.00'))], help_text='Transfer Price por unidad adicional -o total-.')

    #precio_total = models.BooleanField(default=False,  help_text='Seleccionar si el precio no depende de la cantidad.')

    def __str__(self):

        if self.modulo.is_costo_fijo:
            return f'{self.sku} | {self.tp_unidad}'
        
        return f'{self.sku} | {self.precio_base} + (Cant x {self.tp_unidad}) | if Cant <= {self.alcance}'

    class Meta:
        verbose_name = "Escala de Transfer Price"
        verbose_name_plural = "Escalas de Transfer Price"


class Offer(models.Model):
    user = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_DEFAULT)

    subject = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    client = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)

    modulos = models.ManyToManyField(ModuloSaaS, blank=True)

    financing = models.CharField("Financiación", max_length=2, choices=settings.FINANCING, blank=False, \
        default=settings.FINANCING[0][0], help_text="Meses de financiación.")
    hardware = models.CharField(max_length=1, choices=settings.HARDWARE, blank=False, \
        default=settings.HARDWARE[0][0], help_text="Utilizará hardware propio (SPEC) o de terceros?")
    tipo_venta = models.CharField("Tipo de venta", max_length=1, choices=settings.SELLER, blank=False, \
        default=settings.SELLER[0][0], help_text="Quién efectúa la venta?")

    empleados = models.PositiveIntegerField("Cantidad de empleados", default=1, validators=[MinValueValidator(1)])


    def get_TP_modulo(self, modulo):
        """ Return the Transfer Price of an specific module """

        #get all scales of current module
        escalas = EscalaTransferPrice.objects.filter(modulo=modulo)
        
        #if module hasn't scales, return value of module
        if modulo.is_costo_fijo and escalas:
            return escalas[0].tp_unidad

        #escalas con mayor precio. Importa la primera
        escalas_gt = escalas.filter(alcance__gte = self.empleados).order_by('alcance')

        #if module has ranges but hasn't var per unit, return the appropiate
        if modulo.is_range_price and escalas_gt:
            return escalas_gt[0].tp_unidad

        #escalas con menor precio. Importa, la última para saber la cantidad de empleados que no debo tener en cuenta
        escalas_lt = escalas.filter(alcance__lte = self.empleados).order_by('-alcance')

        #precio base de escala actual + la diff entre la cant de emple y la maxima de escala anterior * el precio 
        #unitario de la escala actual
        module_price = escalas_gt[0].precio_base + (self.empleados - escalas_lt[0].alcance) * escalas_gt[0].tp_unidad

        return module_price

    @property    
    def TP_total(self):
        """ Returns the transfer price of all modules of the current offer """
        return sum([self.get_TP_modulo(modulo) for modulo in self.modulos.all()])

    @property
    def TP_mensual_UE(self):
        """ Return -in Euros- the Transfer price of all modules out of number of months """
        return round(self.TP_total / int(self.financing), 2)
    
    @property
    def TP_mensual_USD(self):
        return functions.convert_price(self.TP_mensual_UE, settings.UE_TO_USD)

    def get_margin_or_rebate(self, margin_or_rebate):
        """ returns the margin or rebate of a specific seller """
        margins = Margin.objects.filter(
            Q(tipo_venta=self.tipo_venta),
            Q(hardware=self.hardware),
            Q(financing=self.financing)
            )
        
        if not margins:
            return 0

        return getattr(margins[0], margin_or_rebate, 0)

    @property
    def margen_spec(self):
        return self.get_margin_or_rebate("margin_spec")

    @property
    def margen_integrador(self):
        return self.get_margin_or_rebate("margin_integrador")

    @property
    def margen_mayorista(self):
        return self.get_margin_or_rebate("margin_mayorista")

    @property
    def rebate(self):
        return self.get_margin_or_rebate("rebate")
    

    def __str__(self):
        return f'{self.client} | {self.subject}'

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"
