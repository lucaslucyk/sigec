from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from operator import __or__ as OR
from functools import reduce
from django.conf import settings

from apps.saas.models import Offer, ModuloSaaS
from apps.saas.forms import OfferForm

import json
from django.core.serializers.json import DjangoJSONEncoder
import csv

def get_precios(request, tipo_venta, plan, hardware, modulos, empleados, extra_context=None):

    if not empleados:
        return JsonResponse({"form": {"vm_por_capita": float(0)}})

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
        form = {
            
            "tipo_de_venta": dict(settings.SELLER).get(offer.tipo_venta),
            "plan": dict(settings.FINANCING).get(offer.financing),
            "hardware": dict(settings.HARDWARE).get(offer.hardware),
            "empleados": empleados,
            "modulos": [modulo.nombre for modulo in offer.modulos.all()],
            
            ### valores

            "tp_mensual": float(offer.TP_mensual),
            "soft_host_mant_hd": float(offer.pv_mensual),
            "implementacion": float(offer.implementacion),

            "vm_por_capita": float(offer.pv_por_capita),
        }

        Offer.objects.get(id=offer.id).delete()

    except:
        #delete all objects if raises an global error
        #only for can enter in django-amdin and haven't index error
        Offer.objects.all().delete()
        form = {}
    
    context = {
        "form": form,
    }

    #return context data
    return JsonResponse(context)


def offer_create(request):
    
    context = {
        "form": {},
    }


    return render(request, "saas/saas.html", context)

def generate_graph(request, tipo_venta, plan, hardware, modulos, empleados, fileName="last_graph.csv"):

    offer = Offer.objects.create(
        tipo_venta = tipo_venta,
        financing = plan,
        hardware = hardware,
        )

    if modulos != '*':
        qs = [Q(nombre=modulo) for modulo in modulos.split("-")]
        offer.modulos.set(ModuloSaaS.objects.filter(reduce(OR, qs)))
    else:
        offer.modulos.set(ModuloSaaS.objects.all())

    results_capita = [("capitas", "precio_capita", "hosting", "cuota_mensual\n")]

    for i in range(1, empleados +1):

        offer.empleados = i
        results_capita.append((str(i), str(offer.pv_por_capita).replace(".", ","), str(offer.pv_mensual).replace(".", ",") + '\n' ))
    
    Offer.objects.get(id=offer.id).delete()

    with open(fileName, mode="w", encoding="utf-8") as file:
        file.writelines([";".join(res) for res in results_capita])

    return HttpResponse(f'File generado con {empleados} empleados!')
        

