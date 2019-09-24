from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from apps.data.models import Cliente, Moneda, Categoria, Software
from apps.data.modules.constantes import CONDIC_OFERTAS
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.db.models import Q

class Grupo(models.Model):

    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to='imgs_grupo/', help_text="Para usarla en el producto si no tiene imagen.")

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

class Producto(models.Model):

    codigo = models.CharField(max_length=50, unique=True)
    costo = models.DecimalField("Precio", default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text='')
    activo = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.SET_NULL)
    software_compatible = models.ManyToManyField(Software, blank=True)

    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to='imgs_producto/', help_text="Si no se carga, usa la imagen del grupo.")
    #descripcion = models.CharField(unique=True, blank=False, max_length=255)
    descripcion = models.TextField(blank=False)

    @mark_safe
    def img_display(self):
        if self.imagen:
            return mark_safe(f'<img src="{self.imagen.url}" alt="Imagen {self.codigo}" height="42" width="42" />')
        elif self.grupo.imagen:
            return mark_safe(f'<img src="{self.grupo.imagen.url}" alt="Imagen {self.grupo.nombre}" height="42" width="42" />')
        else:
            return mark_safe('<a href="''"></a>')
    img_display.short_description = "Imagen"

    def get_sw_compatible(self):
        return ", ".join([sw.nombre for sw in self.software_compatible.all()])
    get_sw_compatible.short_description = "Software compatible"

    def get_short_descrip(self):
        return "{}{}".format(self.descripcion[:100], "..." if len(self.descripcion)>100 else "")
    get_short_descrip.short_description = "Descripcion"

    def __str__(self):
        return "{} | {}{}".format(self.codigo, self.descripcion[:100], "..." if len(self.descripcion)>100 else "")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Oferta(models.Model):
    usuario = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_DEFAULT)

    asunto = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True, null=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, null=True, blank=True, default=1, on_delete=models.CASCADE)
    tasa_cambio = models.DecimalField("Tasa de cambio", default=1.00, max_digits=10, decimal_places=2)
    oc_autorizacion = models.FileField("OC - Aprobacion", null=True, blank=True, upload_to='oc_autoriz/ofertas/', help_text="Se agrega al obtener la OC o aprobación del cliente.")
    facturado = models.BooleanField(default=False)

    def existe_categoria(self, categ):
        return True if LineaOferta.objects.filter(Q(oferta=self.id) & Q(producto__categoria__nombre=categ)) else False
        
    def costo_sin_descuento(self):
        '''Costo total de la oferta sin aplicar descuentos'''
        lineas = LineaOferta.objects.filter(oferta=self.id)
        if (len(lineas) == 0):
            return 0
            
        valorFinal = 0
        for val in lineas:
            valorFinal += val.costo_custom * val.cantidad * self.tasa_cambio if val.costo_custom else val.producto.costo * val.cantidad * self.tasa_cambio
        return round(valorFinal,2)
    costo_sin_descuento.short_description = "Costo Sin Descuento"

    def get_categoria_sin_descuento(self, categ):
        '''Costo sin descuento aplicado'''
        if categ == "TOTAL":
            return self.costo_sin_descuento()

        lineas = LineaOferta.objects.filter(
                Q(oferta=self.id) & Q(producto__categoria__nombre=categ)
            )
        if not lineas:
            return 0
        valor_categoria = 0
        for val in lineas:
            valor_categoria += val.costo_custom * val.cantidad * self.tasa_cambio if val.costo_custom else val.producto.costo * val.cantidad * self.tasa_cambio
        return round(valor_categoria,2)

    def get_descuentos(self):
        ''' Retorna un diccionario con todos los descuentos aplicados a cada categoria '''
        descuentos = Descuento.objects.filter(oferta=self.id)
        desc = {}
        for d in descuentos:
            if d.todas:
                desc["TOTAL"] = d.descuento
            else:
                categorias = d.categoria.all()
                for categoria in categorias:
                    desc[categoria.nombre] = d.descuento
        return desc

    def get_descuento_categoria(self, categ):
        '''Retorna el valor de descuento a una categoría específica en formato Decimal("15.00"), donde 15 es el % de descuento'''
        desc = self.get_descuentos()
        if categ in desc.keys():
            return desc.get(categ)
        else:
            return 0

    def get_costo_categoria(self, categ):
        '''Otorga el costo de una categoria con el descuento aplicado'''
        real = self.get_categoria_sin_descuento(categ) #if categ != "TOTAL" else 0
        multiplo = -((self.get_descuento_categoria(categ) - 100 ) / 100)
        return round(real * multiplo,2)
    
    def get_total_descuentos(self):
        '''Returna el monto de todas los descuentos aplicados.'''
        desc = self.get_descuentos()
        val = 0
        if desc:
            for k in desc.keys():
                val += self.get_categoria_sin_descuento(k) - self.get_costo_categoria(k)
        return round(val,2)
    get_total_descuentos.short_description = "Total descuentos"

    def costo_total(self):
        '''Costo total de la oferta, incluyendo descuentos.'''
        total_sd = self.costo_sin_descuento()
        #return "%.02f" % (total_sd - self.get_total_descuentos())
        return round(total_sd - self.get_total_descuentos(),2)
    costo_total.short_description = "Costo Total"

    @mark_safe
    def fileLink(self):
        if self.oc_autorizacion:
            return mark_safe(f'<a href="{self.oc_autorizacion.url}" target="_blank">Enlace</a>')
        else:
            return mark_safe('<a href="''"></a>')
    fileLink.allow_tags = True
    fileLink.short_description = "Link OC-Aprob"

    def user_names(self):
            return f'{self.usuario.first_name} {self.usuario.last_name}'
    user_names.short_description = "Usuario"

    def __str__(self):
        return f'{self.cliente} | {self.asunto}'

    class Meta:
        verbose_name = "Oferta"
        verbose_name_plural = "Ofertas"

class LineaOferta(models.Model):
    oferta = models.ForeignKey(Oferta, null=True, blank=False, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    costo_custom = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text='')

    @mark_safe
    def link_oferta(self):
        link = reverse("admin:cotizaciones_oferta_change", args=[self.oferta.id]) #model name has to be lowercase
        return mark_safe(f'<a href="{link}">{self.oferta.asunto}</a>')
    link_oferta.allow_tags = True
    link_oferta.short_description = "Presupuesto"

    def __str__(self):
        return f'PDV: {self.producto.costo} | {self.cantidad} x {self.producto}'

    class Meta:
        verbose_name = 'Producto ofertado'
        verbose_name_plural = 'Productos ofertados'

class Descuento(models.Model):
    oferta = models.ForeignKey(Oferta, null=True, blank=False, on_delete=models.CASCADE)
    descuento = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text='Valor del porcentaje.')
    categoria = models.ManyToManyField(Categoria, blank=True, help_text='Categorías a la que se aplicaran el descuento.')
    todas = models.BooleanField(default=False, help_text='Seleccionar si el descuento es sobre todas las categorías.')

    def __str__(self):
        return f'{self.descuento}%'

    class Meta:
        verbose_name = 'Descuento'
        verbose_name_plural = 'Descuentos'

class Condiciones_Custom(models.Model):
    oferta = models.ForeignKey(Oferta, null=True, blank=False, on_delete=models.CASCADE)

    validez_de_la_oferta = models.TextField(blank=False, default=CONDIC_OFERTAS[1].get('contenido'))
    forma_de_pago = models.TextField(blank=False, default=CONDIC_OFERTAS[3].get('contenido'))
    garantia = models.TextField(blank=False, default=CONDIC_OFERTAS[5].get('contenido'))
    precios = models.TextField(blank=False, default=CONDIC_OFERTAS[7].get('contenido'))
    instalacion = models.TextField(blank=False, default=CONDIC_OFERTAS[9].get('contenido'))
    facturacion = models.TextField(blank=False, default=CONDIC_OFERTAS[11].get('contenido'))

    def __str__(self):
        return f'{self.oferta.asunto}'

    class Meta:
        verbose_name = 'Condición Personalizada'
        verbose_name_plural = 'Condiciones Personalizadas'