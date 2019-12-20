from django.contrib import admin
from apps.cotizaciones.models import Grupo, Producto, Oferta, LineaOferta, Descuento, Condiciones_Custom
from apps.data.modules.functions import crea_excel_oferta, import_products
from django.contrib import messages
from django.conf import settings
from dynamic_raw_id.admin import DynamicRawIDMixin
#from django.contrib.auth.models import User

import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.db.models.functions import TruncDay, Trunc, TruncMonth
from django.http import JsonResponse
from django.urls import path

from django.db.models import Q

# #from django.core.exceptions import ValidationError
# #from django import forms

# from django.contrib.auth.admin import UserAdmin

# UserAdmin.list_display += ('body_font',)  # don't forget the commas
# UserAdmin.list_filter += ('body_font',)
# fieldsets = (
#     ('Personalizadas', {
#         'classes': ('extrapretty',),
#         'fields': ('body_font',),
#     }),
# )
# UserAdmin.fieldsets += fieldsets

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



    actions = ["importar_productos"]

    def importar_productos(self, request, queryset):
        try:
            erroneos = import_products(settings.FILE_PRODUCTOS)
            if (erroneos):
                msj = ", ".join(str(val) for val in erroneos)
                messages.add_message(request, messages.WARNING, 'Error al importar los productos {}'.format(msj))
            else:
                messages.add_message(request, messages.SUCCESS, 'Productos importados correctamente!')

        except Exception as err:
            messages.add_message(request, messages.ERROR, 'ERROR importando productos. {}'.format(err))
        return
        #return import_products()
    importar_productos.short_description = "Importar desde CSV"

class ItemsInLine(DynamicRawIDMixin, admin.StackedInline):
    model = LineaOferta
    extra = 1
    ordering = ("producto__codigo",)
    #raw_id_fields = ("producto",)
    autocomplete_fields = ["producto"]
    #dynamic_raw_id_fields = ('producto',)

class DescuentoAdmin(admin.ModelAdmin):
    search_fields = ["descuento", "categoria__nombre"]
    ordering = ("descuento", "categoria__nombre")
    #autocomplete_fields = ["categoria__nombre"]

class DescuentosInLine(admin.StackedInline):
    model = Descuento
    extra = 0
    ordering = ("descuento",)
    autocomplete_fields = ["categoria"]

class CondicionesInLine(admin.StackedInline):
    model = Condiciones_Custom
    extra = 0
    fieldsets = (
        ('Editar condiciones', {
            'classes': ('collapse',),
            'fields': ('validez_de_la_oferta','forma_de_pago', 'garantia', 'precios', 'instalacion', 'facturacion'),
        }),
    )

class OfertaAdmin(admin.ModelAdmin):
    #form = OfertaForm

    inlines = [CondicionesInLine, DescuentosInLine, ItemsInLine]

    list_display = ("id", "asunto", "fecha","cliente","moneda","tasa_cambio","costo_total")#, "facturado", "fileLink", "usuario")
    readonly_fields = ['fileLink']
    list_filter = ["moneda", "facturado", "usuario"]
    search_fields = [
        'cliente__nombre', "asunto", "id", "usuario__first_name", "usuario__last_name",
        "usuario__username", "moneda__codigo", "moneda__nombre"
    ]
    list_display_links = ["id", "asunto"]
    #fields = ( "asunto", "cliente", "moneda", "tasa_cambio", "facturado", "oc_autorizacion")
    #list_editable =["facturado"]
    #ordering = ("id",'asunto')
    #raw_id_fields = ("cliente",)
    autocomplete_fields = ['cliente', 'moneda']
    ordering = ("fecha",)
    list_per_page = 50

    save_as = True
    save_on_top = True
    change_list_template = 'ofertas_change_list.html'

    fieldsets = (
        (None, {
            'fields': ('asunto', 'cliente', 'moneda', 'tasa_cambio',)
        }),
        ('Facturación', {
            'classes': ('collapse',),
            'fields': ('facturado', 'oc_autorizacion',),
        }),
    )

    actions = ["crea_excel"]

    def crea_excel(self, request, queryset):
        return crea_excel_oferta(queryset)
    crea_excel.short_description = "Generar Excel"

    def changelist_view(self, request, extra_context=None):
        # Aggregate new subscribers per day
        chart_data = self.chart_data(qs_filter=request.GET)
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        extra_urls = [
            path("chart_data/", self.admin_site.admin_view(self.chart_data_endpoint))
        ]
        # NOTE! Our custom urls have to go before the default urls, because they
        # default ones match anything.
        return extra_urls + urls

    # JSON endpoint for generating chart data that is used for dynamic loading
    # via JS.
    def chart_data_endpoint(self, request):
        chart_data = self.chart_data(qs_filter=request.GET) #Siempre da un QD vacio, para reiniciar el graph
        return JsonResponse(list(chart_data), safe=False)

    def chart_data(self, qs_filter=None):
        #print("Fields order: ", self.list_display)

        if not qs_filter :   #retorno todos los elementos por cualquier error de req
            return (
                #Oferta.objects.annotate(date=Trunc("fecha", "month"))
                Oferta.objects.annotate(date=TruncDay("fecha"))
                .values("date")
                .annotate(y=Count("id"))
                .order_by('-date')
            )
        qs = Q()

        #Condiciones para el campo de busqueda.
        if "q" in qs_filter.keys():
            search_fields = [
                'cliente__nombre', "asunto", "id", "usuario__first_name", 
                "usuario__last_name", "usuario__username", "moneda__codigo", "moneda__nombre"
            ]
            condic = {}
            for f in search_fields:
                condic[f'{f}__icontains'] = qs_filter.get("q")
            for key, value in condic.items():
                qs.add(Q(**{key: value}), Q.OR)

        #Condiciones de filtro
        for k,v in qs_filter.dict().items():
            #excluyo el campo de busqueda (q) y orden (o)
            if k is not "q" and k is not "o":
                qs.add(Q(**{k:v}), Q.AND)

        return (
            Oferta.objects.filter(qs).annotate(date=TruncDay("fecha"))
            .values("date")
            .annotate(y=Count("id"))
            .order_by("-date")
        )
        
        
    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        #if obj.tasa_cambio < 1:
        #raise ValidationError("La tasa de cambio de menor a 1.")
        obj.save()

class LineaAdmin(admin.ModelAdmin):

    list_display = ("link_oferta", "cantidad", "producto", "costo_custom")
    search_fields = ["oferta__moneda__codigo", "oferta__cliente__nombre", "producto__codigo", "producto__categoria__nombre", "producto__descripcion"]
    list_filter = ["oferta__cliente__nombre"]
    #change_list_template = 'itemsPresup_change_list.html'

    actions = None
    def has_add_permission(self, request, obj=None):
        return False

    #def has_delete_permission(self, request, obj=None):
        #return True if request.user.is_superuser else False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(LineaOferta, LineaAdmin)