from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.urls import reverse
from apps.data.models import Cliente, Moneda, Categoria, Software

class Grupo(models.Model):

    nombre = models.CharField(max_length=50, unique=True, blank=False, null=False)
    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to='imgs_grupo/', help_text="Para usarla en el producto si no tiene imagen.")

    def __str__(self):
        return f'{self.nombre}'

    class Meta:
        verbose_name = "Grupo"
        verbose_name_plural = "Grupos"

class Producto(models.Model):

    codigo = models.CharField(max_length=20, unique=True)
    costo = models.IntegerField()
    activo = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.SET_NULL)
    software_compatible = models.ManyToManyField(Software, blank=True)

    imagen = models.ImageField("Imagen", null=True, blank=True, upload_to='imgs_producto/', help_text="Si no se carga, usa la imagen del grupo.")
    descripcion = models.CharField(unique=True, blank=False, max_length=255)

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
        return "{}{}".format(self.descripcion[:50], "..." if len(self.descripcion)>50 else "")
    get_short_descrip.short_description = "Descripcion"

    def __str__(self):
        return "{}{}".format(self.descripcion[:50], "..." if len(self.descripcion)>50 else "")

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

class Oferta(models.Model):
    usuario = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_DEFAULT)

    asunto = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateField(auto_now_add=True, null=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.CASCADE)
    moneda = models.ForeignKey(Moneda, null=True, blank=True, default=1, on_delete=models.CASCADE)
    tasa_cambio = models.DecimalField(default=1.00, max_digits=10, decimal_places=2)
    oc_autorizacion = models.FileField("OC - Aprobacion", null=True, blank=True, upload_to='oc_autoriz/ofertas/', help_text="Se agrega al obtener la OC o aprobación del cliente.")
    facturado = models.BooleanField(default=False)

    def costo_total(self):
        lineas = LineaOferta.objects.filter(oferta=self.id)
        if (len(lineas) == 0):
            return 0
            
        valorFinal = 0
        for val in lineas:
            valorFinal += val.costo_custom * val.cantidad if val.costo_custom else val.producto.costo * val.cantidad * self.tasa_cambio
        return valorFinal
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
    cantidad = models.IntegerField(default=1)
    costo_custom = models.DecimalField(default=0, max_digits=10, decimal_places=2, help_text='')

    @mark_safe
    def link_oferta(self):
        link = reverse("admin:cotizaciones_oferta_change", args=[self.oferta.id]) #model name has to be lowercase
        return mark_safe(f'<a href="{link}">{self.oferta.asunto}</a>')
    link_oferta.allow_tags = True
    link_oferta.short_description = "Presupuesto"

    def __str__(self):
        return "%s x %s"%(self.cantidad, self.producto)

    class Meta:
        verbose_name = 'Producto ofertado'
        verbose_name_plural = 'Productos ofertados'