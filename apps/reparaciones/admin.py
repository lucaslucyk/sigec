from django.contrib import admin
from apps.reparaciones.models import FamiliaRepuesto, Repuesto, Presupuesto, LineaPresupuesto
from django.http import HttpResponse
import csv#, openpyxl
from django.conf import settings
from apps.data.modules.functions import crea_excel_presupuesto
#import re
#from django.contrib import messages
#from django.urls import reverse

admin.site.site_header = "SIGeC - v{}".format(settings.VERSION)
admin.site.site_title = "Sistema Integrado de Gestión de Cotizaciones"
admin.site.index_title = "SIGeC | Creado por Lucas Lucyk"

class FamiliaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ["nombre"]
    ordering = ("nombre",)

class RepuestoAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre", "familia", "costo")
    list_filter = ["familia"]
    search_fields = ["familia__nombre", "nombre", "codigo"]
    ordering = ('familia','nombre')
    list_display_links = ["codigo", "nombre"]
    autocomplete_fields = ["familia"]

class ItemsInLine(admin.StackedInline):
    model = LineaPresupuesto
    extra = 2
    ordering = ("repuesto__familia",'repuesto__nombre')
    #raw_id_fields = ("repuesto",)
    autocomplete_fields = ["repuesto"]

class PresupAdmin(admin.ModelAdmin):
    inlines = [ItemsInLine]

    list_display = ("id", "asunto", "fecha","cliente","moneda","tasa_cambio","costo_total", "facturado", "fileLink", "usuario")
    readonly_fields = ['fileLink']
    list_filter = ["fecha","moneda", "facturado", "usuario"]
    search_fields = ['cliente__nombre', "asunto", "id", "usuario__first_name", "usuario__last_name", "usuario__username"]
    list_display_links = ["id", "asunto"]
    list_editable =["facturado"]
    ordering = ("id",'asunto')
    #raw_id_fields = ("cliente",)
    autocomplete_fields = ['cliente', 'moneda']
    #ordering = ("fecha",)
    list_per_page = 50

    actions = ["export_as_csv", "crea_excel"]
    save_as = True
    save_on_top = True
    change_list_template = 'presup_change_list.html'

    fields = ( "asunto", "cliente", "moneda","tasa_cambio", "facturado", "oc_autorizacion")
    
    def save_model(self, request, obj, form, change):
        obj.usuario = request.user
        obj.save()

    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Exportar items"
    #generar_reporte.short_description = "Generar CSV"

    def crea_excel(self, request, queryset):
        return crea_excel_presupuesto(queryset)

    crea_excel.short_description = "Generar Excel"

class LineaAdmin(admin.ModelAdmin):

    list_display = ("presup_link", "cantidad", "repuesto", "costo_custom")
    search_fields = ["presupuesto__moneda__codigo", "presupuesto__cliente__nombre", "repuesto__nombre", "repuesto__familia__nombre"]
    change_list_template = 'itemsPresup_change_list.html'

    actions = None
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(FamiliaRepuesto, FamiliaAdmin)
admin.site.register(Repuesto, RepuestoAdmin)
admin.site.register(Presupuesto, PresupAdmin)
admin.site.register(LineaPresupuesto, LineaAdmin)