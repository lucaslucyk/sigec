from django.contrib import admin
from apps.saas.models import *

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
	list_display = ('tipo_venta', 'plan', 'hardware', 'empleados', 
		#'pvs_mensual', 'pvs_total', 
		'pv_capita', 'pv_mensual', 'pv_total',
		'costo_capita', 'costo_mes', 'costo_total',
		'margen_bruto',
	)
	list_filter =  ('tipo_venta', 'plan', 'hardware')


@admin.register(TipoVenta)
class TipoVentaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'directa')
	list_filter = ('directa', )

@admin.register(Descuento)
class DescuentoAdmin(admin.ModelAdmin):
	list_display = ('tipo_venta', 'porcentaje')
	list_filter = ('tipo_venta', )

@admin.register(EscalaPrecio)
class EscalaPrecioAdmin(admin.ModelAdmin):
	list_display = ('plan', 'display_tdv', 'hardware', 'alcance', 'precio_base',
		 'tp_unidad', '__str__',
	)
	list_filter = ('plan', 'hardware', 'tipos_de_venta')


admin.site.register(Plan)
admin.site.register(Hardware)
#admin.site.register(EscalaPrecio)
#admin.site.register(Descuento)
#admin.site.register(ModuloSaaS)

# @admin.register(EscalaTransferPrice)
# class EscalaTransferPriceAdmin(admin.ModelAdmin):
# 	list_display = ('sku', 'modulo', 'precio_base', 'alcance', 'tp_unidad')
# 	list_filter =  ('modulo',)

# @admin.register(Margin)
# class MarginAdmin(admin.ModelAdmin):
# 	list_display = ('tipo_venta', 'financing', 'hardware', 'margin_spec', 
# 		'margin_integrador', 'margin_mayorista', 'rebate_mayorista', 'rebate_partner')
# 	ordering = ('financing', 'hardware', 'tipo_venta')
# 	list_filter = ('financing', 'hardware', 'tipo_venta')
# 	search_fields = ('financing', 'hardware', 'tipo_venta')

# @admin.register(Offer)
# class OfferAdmin(admin.ModelAdmin):
# 	list_display = (
# 		'empleados', 'financing', 'tipo_venta', 'hardware',
# 		'TP_mensual', 
# 		'pvp_spec', 
# 		'pvs_mayorista',
# 		'pvs_partner',
# 		'pvs_end_user', 'implementacion', 
# 		#'pv_mensual', 
# 		'pv_por_capita', 'comision_mensual',
# 		'rebate_mayorista_usd',
# 		'rebate_partner_usd',
# 		)

# 	fieldsets = (
# 		(None, {
# 			'fields': ('subject', 'client', 'tipo_venta', 'financing', 'hardware', 'empleados', 'modulos')
# 		}),
# 	)
# 	autocomplete_fields = ['client',]

# 	"""
# 	formfield_overrides = {
#         models.IntegerField: {'widget': SlideForm},
#     }
#     """

# 	def save_model(self, request, obj, form, change):
# 		obj.user = request.user
# 		#if obj.tasa_cambio < 1:
# 		#raise ValidationError("La tasa de cambio de menor a 1.")
# 		obj.save()

# 	#readonly_fields = ['margen_spec', 'margen_mayorista', 'margen_integrador']


