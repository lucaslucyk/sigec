from django.contrib import admin
from apps.saas.models import Offer, Margin, ModuloSaaS, EscalaTransferPrice

@admin.register(EscalaTransferPrice)
class EscalaTransferPriceAdmin(admin.ModelAdmin):
	list_display = ('sku', 'modulo', 'precio_base', 'alcance', 'tp_unidad')
	list_filter =  ('modulo',)

@admin.register(Margin)
class MarginAdmin(admin.ModelAdmin):
	list_display = ('tipo_venta', 'financing', 'hardware', 'margin_spec', 
		'margin_integrador', 'margin_mayorista', 'rebate_mayorista', 'rebate_partner')
	ordering = ('financing', 'hardware', 'tipo_venta')
	list_filter = ('financing', 'hardware', 'tipo_venta')
	search_fields = ('financing', 'hardware', 'tipo_venta')

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
	list_display = (
		'empleados', 'financing', 'tipo_venta', 'hardware',
		'TP_mensual', 
		'pvp_spec', 
		'pvs_mayorista',
		'pvs_partner',
		'pvs_end_user', 'implementacion', 
		#'pv_mensual', 
		'pv_por_capita', 'comision_mensual',
		'rebate_mayorista_usd',
		'rebate_partner_usd',
		)

	fieldsets = (
		(None, {
			'fields': ('subject', 'client', 'tipo_venta', 'financing', 'hardware', 'empleados', 'modulos')
		}),
	)
	autocomplete_fields = ['client',]

	"""
	formfield_overrides = {
        models.IntegerField: {'widget': SlideForm},
    }
    """

	def save_model(self, request, obj, form, change):
		obj.user = request.user
		#if obj.tasa_cambio < 1:
		#raise ValidationError("La tasa de cambio de menor a 1.")
		obj.save()

	#readonly_fields = ['margen_spec', 'margen_mayorista', 'margen_integrador']

admin.site.register(ModuloSaaS)