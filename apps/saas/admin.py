from django.contrib import admin
from apps.saas.models import *

@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
	list_display = ('tipo_venta', 'plan', 'empleados', 
		#'pvs_mensual', 'pvs_total', 
		'pv_capita', 'pv_mensual', 'pv_total',
		'costo_capita', 'costo_mes', 'costo_total',
		'margen_bruto', 'moneda' #, 'hardware'
	)
	list_filter =  ('tipo_venta', 'plan') #, 'hardware')


@admin.register(TipoVenta)
class TipoVentaAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'moneda', 'directa')
	list_filter = ('directa', 'moneda__codigo')

# @admin.register(Descuento)
# class DescuentoAdmin(admin.ModelAdmin):
# 	list_display = ('tipo_venta', 'porcentaje')
# 	list_filter = ('tipo_venta', )

@admin.register(EscalaPrecio)
class EscalaPrecioAdmin(admin.ModelAdmin):
	list_display = ('plan', 'display_tdv', 'minimo', 'alcance', 'precio_base',
		 'tp_unidad', 'descuento_terceros', '__str__', #'hardware'
	)
	list_filter = ('plan', 'tipos_de_venta') #,'hardware')


admin.site.register(Plan)
#admin.site.register(Hardware)



