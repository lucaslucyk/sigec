from django.contrib import admin
from apps.data.models import Comercial, Contrato, Moneda, Cliente, Categoria, Software
from django.conf import settings
from apps.data.modules.functions import updateClients
from django.contrib import messages
#from django.http import HttpResponse
#import csv, openpyxl
#import re 
#from django.urls import reverse

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





admin.site.site_header = "SIGeC - v{}".format(settings.VERSION)
admin.site.site_title = "Sistema Integrado de Gestión de Cotizaciones"
admin.site.index_title = "SIGeC | Creado por Lucas Lucyk"

class ComercialAdmin(admin.ModelAdmin):
    list_display = ("nombre_apellido", "email")
    search_fields = ["nombre_apellido", "email"]
    ordering = ("nombre_apellido",)

class ContratoAdmin(admin.ModelAdmin):
    list_display = ("cobertura",)
    search_fields = ["cobertura"]
    ordering = ("cobertura",)

class MonedaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nombre")
    search_fields = ["codigo", "nombre"]

class ClienteAdmin(admin.ModelAdmin):
    list_display = ("id_sage", "nombre", "comercial","get_sla", "vencimiento_sla", "mantenim_activo")
    list_filter = ["comercial", "sla"]
    search_fields = ['nombre', "sla__cobertura", "comercial__nombre_apellido", "id_sage"]
    ordering = ('nombre','id_sage')
    actions = ["update_clients"]
    list_display_links = ['nombre','id_sage']
    list_per_page = 25
    autocomplete_fields = ["sla", "comercial", "moneda"]
    save_as = True
    save_on_top = True
    change_list_template = 'clte_change_list.html'

    def update_clients(self, request, queryset):

        permisos = request.user.groups.values_list('name',flat=True)

        if ("Visualizacion" in permisos):
            messages.add_message(request, messages.WARNING, 'Requiere permisos para importar')
            return

        try:
            #print(settings.FILE_CLIENTES)
            erroneos = updateClients(settings.FILE_CLIENTES)
            if (erroneos):
                msj = ", ".join(str(val) for val in erroneos)
                messages.add_message(request, messages.WARNING, 'Error en SLA o Comercial de los clientes {}'.format(msj))
            else:
                messages.add_message(request, messages.SUCCESS, 'Clientes importados correctamente')

        except Exception as err:
            messages.add_message(request, messages.ERROR, 'ERROR importando clientes. {}'.format(err))
            pass
        return

    update_clients.short_description = "Importar desde CSV"

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ["nombre"]
    ordering = ("nombre",)

class SoftwareAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ["nombre"]
    ordering = ("nombre",)

admin.site.register(Comercial, ComercialAdmin)
admin.site.register(Contrato, ContratoAdmin)
admin.site.register(Moneda, MonedaAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Software, SoftwareAdmin)