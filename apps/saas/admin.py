from django.contrib import admin
from apps.saas.models import Offer, Margin, ModuloSaaS, EscalaTransferPrice
# Register your models here.

@admin.register(Margin)
class MarginAdmin(admin.ModelAdmin):
	list_display = ('financing', 'hardware', 'tipo_venta', 'margin_spec', 'margin_integrador', 'margin_mayorista')
	ordering = ('financing', 'hardware', 'tipo_venta')
	list_filter = ('financing', 'hardware', 'tipo_venta')
	search_fields = ('financing', 'hardware', 'tipo_venta')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
	list_display = ('empleados', 'TP_total', 'TP_mensual_USD', 'margen_spec', 'margen_integrador', 'margen_mayorista', 'rebate')

admin.site.register(ModuloSaaS)
admin.site.register(EscalaTransferPrice)