from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from apps.saas.models import Offer, ModuloSaaS
from django.db.models import Q
from operator import __or__ as OR
from functools import reduce
from django.conf import settings

def sample_text(request, tipo_venta, plan, hardware, modulos, empleados):

	offer = Offer.objects.create(
			tipo_venta = tipo_venta,
			financing = plan,
			hardware = hardware,
			empleados = empleados,
			)

	if modulos != '*':
		qs = [Q(nombre=modulo) for modulo in modulos.split("-")]
		offer.modulos.set(ModuloSaaS.objects.filter(reduce(OR, qs)))

	else:
		offer.modulos.set(ModuloSaaS.objects.all())

	context = {}
	try:
		context = {
			
			"Tipo de venta": dict(settings.SELLER).get(offer.tipo_venta),
			"Plan": dict(settings.FINANCING).get(offer.financing),
			"Hardware": dict(settings.HARDWARE).get(offer.hardware),
			"Empleados": empleados,
			"Módulos": [modulo.nombre for modulo in offer.modulos.all()],
			
			"_valores_": "***",

			"Transfer Price Mensual": float(offer.TP_mensual),
			"Soft, Host, Mant & Help Desk": float(offer.pv_mensual),
			"Implementación": float(offer.implementacion),

			"Valor mensual por cápita": float(offer.pv_por_capita),
		}

		Offer.objects.get(id=offer.id).delete()

	except:
		#delete all objects if raises an global error
		#only for can enter in django-amdin and haven't index error
		Offer.objects.all().delete()

	return JsonResponse(context)


	#return HttpResponse("Sample view " + " ".join(modulos) + " " + str(empleados) + str(offer.pv_por_capita))
