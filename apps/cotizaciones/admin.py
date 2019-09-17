from django.contrib import admin
from apps.cotizaciones.models import Grupo, Producto, Oferta, LineaOferta, Descuento
from apps.data.modules.functions import crea_excel_oferta

#from django.core.exceptions import ValidationError
#from django import forms

class GrupoAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ["nombre"]
    ordering = ("nombre",)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "get_short_descrip", "categoria", "grupo", "get_sw_compatible", "costo", "img_display")
    list_filter = ["activo", "categoria", "grupo", "software_compatible"]
    search_fields = ["codigo", "descripcion", "costo", "activo", "categoria__nombre", "grupo__nombre", "software_compatible__nombre"]
    ordering = ('categoria', 'grupo', 'activo', 'codigo')
    #actions = ["update_clients"]
    #list_display_links = ['nombre','id_sage']
    list_per_page = 25
    autocomplete_fields = ["software_compatible", "categoria", "grupo"]
    save_as = True
    save_on_top = True

class ItemsInLine(admin.StackedInline):
    model = LineaOferta
    extra = 1
    ordering = ("producto__codigo",)
    #raw_id_fields = ("repuesto",)
    autocomplete_fields = ["producto"]

class DescuentoAdmin(admin.ModelAdmin):
    search_fields = ["descuento", "categoria__nombre"]
    ordering = ("descuento", "categoria__nombre")
    #autocomplete_fields = ["categoria__nombre"]

class DescuentosInLine(admin.StackedInline):
    model = Descuento
    extra = 0
    ordering = ("descuento",)
    autocomplete_fields = ["categoria"]

class OfertaAdmin(admin.ModelAdmin):
    #form = OfertaForm

    inlines = [DescuentosInLine, ItemsInLine]

    list_display = ("id", "asunto", "fecha","cliente","moneda","tasa_cambio","costo_total")#, "facturado", "fileLink", "usuario")
    readonly_fields = ['fileLink']
    list_filter = ["moneda", "facturado", "usuario"]
    search_fields = ['cliente__nombre', "asunto", "id", "usuario__first_name", "usuario__last_name", "usuario__username", "moneda__codigo", "moneda__nombre" ]
    list_display_links = ["id", "asunto"]
    fields = ( "asunto", "cliente", "moneda", "tasa_cambio", "facturado", "oc_autorizacion")
    #list_editable =["facturado"]
    #ordering = ("id",'asunto')
    #raw_id_fields = ("cliente",)
    autocomplete_fields = ['cliente', 'moneda']
    ordering = ("fecha",)
    list_per_page = 50

    save_as = True
    save_on_top = True
    #change_list_template = 'presup_change_list.html'

    actions = ["crea_excel"]

    def crea_excel(self, request, queryset):
            return crea_excel_oferta(queryset)
    crea_excel.short_description = "Generar Excel"

    # def save_model(self, request, obj, form, change):
    #     if obj.tasa_cambio < 1:
    #         raise ValidationError("La tasa de cambio de menor a 1.")
    #     obj.save()

class LineaAdmin(admin.ModelAdmin):

    list_display = ("link_oferta", "cantidad", "producto", "costo_custom")
    search_fields = ["oferta__moneda__codigo", "oferta__cliente__nombre", "producto__codigo", "producto__categoria__nombre", "producto__descripcion"]
    list_filter = ["oferta__cliente__nombre"]
    #change_list_template = 'itemsPresup_change_list.html'

    actions = None
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(LineaOferta, LineaAdmin)