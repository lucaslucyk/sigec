from django.contrib import admin
from apps.cotizaciones.models import Grupo, Producto, Oferta, LineaOferta

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
    extra = 2
    ordering = ("producto__codigo",)
    #raw_id_fields = ("repuesto",)
    autocomplete_fields = ["producto"]

class OfertaAdmin(admin.ModelAdmin):
    inlines = [ItemsInLine]

    list_display = ("id", "asunto", "fecha","cliente","moneda","tasa_cambio","costo_total", "facturado", "fileLink", "usuario")
    readonly_fields = ['fileLink']
    list_filter = ["moneda", "facturado", "usuario"]
    search_fields = ['cliente__nombre', "asunto", "id", "usuario__first_name", "usuario__last_name", "usuario__username", "producto__codigo", "producto__descripcion", ]
    list_display_links = ["id", "asunto"]
    #list_editable =["facturado"]
    #ordering = ("id",'asunto')
    #raw_id_fields = ("cliente",)
    autocomplete_fields = ['cliente', 'moneda']
    ordering = ("fecha",)
    list_per_page = 50

    #actions = ["export_as_csv", "generar_excel_v2"]
    save_as = True
    save_on_top = True
    #change_list_template = 'presup_change_list.html'

    fields = ( "asunto", "cliente", "moneda", "tasa_cambio", "facturado", "oc_autorizacion")

admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Producto, ProductoAdmin)