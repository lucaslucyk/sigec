import sys, csv, operator, re
from datetime import datetime
from django.http import HttpResponse
from xlsxwriter import Workbook
from django.conf import settings
from apps.data.models import Contrato, Cliente, Comercial
from apps.data.modules.constantes import FORMATOS, CONDIC_PRESUP
from apps.reparaciones.models import LineaPresupuesto
#import openpyxl

##customs process

def updateClients(fileRoot="../update_clients/clientes.csv"):
	
	fileRoot = re.sub(r'\\','/',fileRoot)
	erroneos = []
	with open(fileRoot) as ClientsFile:

		registros = csv.DictReader(ClientsFile, delimiter=';')

		for registro in registros:
			values = {
				'idSage': int(re.sub(r'\.','',registro['Id de empresa'])),
				'nombre': registro['Nombre de la empresa'].title(),
				'mantenimientos': re.sub(r'\,$','',registro['Mantenimientos'].title()).split(", "),
				'vencim': datetime.strptime(registro['Fecha vencimiento del Mantenimiento'], "%d/%m/%Y") if registro['Fecha vencimiento del Mantenimiento'] else datetime.now().replace(month=12, day=31),
				'comercial': registro['Gestor de cuentas']
			}
			
			comerc = None
			mantenim = []

			for mant in values.get("mantenimientos"):
				for item in Contrato.objects.filter(cobertura=mant):
					mantenim.append(item) if item else None

			#Busco al cliente. Si no lo encuentro, lo creo vacío
			try:
				comerc = Comercial.objects.get(nombre_apellido=values['comercial']) if values['comercial'] else None
			except:
				#print ("No se encuentra el SLA o Comercial")
				erroneos.append(values['nombre'])
				continue

			try:
				cliente = Cliente.objects.get(id_sage=values['idSage'])
			except:
				cliente = Cliente()

			##Actualizo los campos del cliente
			cliente.id_sage = values['idSage']
			cliente.nombre = values['nombre']
			cliente.comercial = comerc
			
			cliente.vencimiento_sla = values['vencim']

			#Intento guardar. Si no es posible, informo error
			try:
				cliente.save()
				cliente.sla.set(mantenim)
				cliente.save()
			except:
				if (values['nombre'] not in erroneos):
					erroneos.append(values['nombre'])
		ClientsFile.close()
	return (erroneos)

def format_filas_columnas(sheet):
	################# ANCHO Y ALTO #################
	#ancho de cada columna. De A en adelante >>
	anchuras = (2.86, 5.43, 18.57, 10, 52.29, 5, 7, 5, 7, 5.43)

	for x in range(len(anchuras)):
		sheet.set_column(x, x, anchuras[x])

	#Altos de columnas x..
	#el formato es columna, altura
	alturas = ((8, 18.75), (10, 41.25), (27, 18.75))
	for fila, alto in alturas:
		sheet.set_row(fila, alto)

	################# ANCHO PARA IMPRESION #################
	#1 pagina de ancho y el largo necesario (0)
	sheet.fit_to_pages(1, 0)

def imp_cabeceras(book, sheet, obj, headerFrom=""):
	'''
		Imprime las cabeceras, la imagen del logo y revuelve la posición de la fila donde termina
	'''
	header = {
		"Para": [2,2, book.add_format(FORMATOS.get("headerKeys"))],
		obj.cliente.nombre: [2,3],

		"Presupuesto N°:": [4,2, book.add_format(FORMATOS.get("headerKeys"))],
		obj.id: [4,3, book.add_format(FORMATOS.get("izquierda"))],

		"Fecha": [6,2, book.add_format(FORMATOS.get("headerKeys"))],
		obj.fecha: [6,3,book.add_format(FORMATOS.get("fechaIzq"))],

		"De: {}".format(headerFrom): [6, 9, book.add_format(FORMATOS.get("bajoImg"))],
	}
	#Imprime las cabeceras
	row = 0
	for k,v in header.items():
		sheet.write(*v[:2], k, v[2] if len(v)==3 else None)
		row = v[0]

	################# LOGO #################
	#Insertando logo..
	rutaImg = "{}\\templates\\excel\\logo_spec_170_110.png".format(settings.BASE_DIR)
	sheet.insert_image('G2', rutaImg, {'x_scale': 0.84, 'y_scale': 0.84, "x_offset": 6})
	################# FIN LOGO #################

	return row

def imp_linea_vacia(book, sheet, row, col, final=False, condiciones=False):
	'''
		Imprime una línea vacía con los formatos correspondiente.
	'''

	if condiciones:
		formatosItems = (
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(FORMATOS.get("linea_inf") if final else {}),
			book.add_format(dict(**FORMATOS.get("item_BD"), **FORMATOS.get("linea_inf") if final else {})),
			)
	else:
		#formateando bordes...
		formatosItems = (
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_SB"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_BI"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_SB"), **FORMATOS.get("linea_inf") if final else {})),
			book.add_format(dict(**FORMATOS.get("item_BD"), **FORMATOS.get("linea_inf") if final else {})),
			)
	#imprime linea vacia 
	for c in range(len(formatosItems)):
		sheet.write(row, c+col, "", formatosItems[c])

def imp_linea_total(book, sheet, row, col, moneda, initialRow, lineas, final=False, grupo=""):
	'''
		Imprime una línea de total con los formatos correspondientes
	'''
	sheet.write(row, col, "", book.add_format(FORMATOS.get("item_BI")))
	sheet.write(row, col+1, "", book.add_format(FORMATOS.get("item_BI")))
	sheet.write(row, col+2, "_____ TOTAL OFERTA {}_____".format(grupo.upper()), book.add_format(dict(
																						**FORMATOS.get("item_BI"),
																						**FORMATOS.get("negrita"),
																						)))
	sheet.write(row, col+3, "", book.add_format(FORMATOS.get("item_BI")))
	sheet.write(row, col+5, moneda, book.add_format(FORMATOS.get("item_BI")))
	sheet.write_formula(row, col+6, "SUM(I{}:I{})".format(initialRow+1, initialRow+lineas), book.add_format(FORMATOS.get("item_SB")))
	sheet.write(row, col+7, "+ IVA", book.add_format(FORMATOS.get("item_BD")))

def imp_condiciones(book, sheet, row, col, tipo="presupuesto"):
	'''
		Imprime las condiciones comerciales.
	'''

	sheet.merge_range(row, col, row, col+7, "CONDICIONES COMERCIALES", book.add_format(FORMATOS.get("headerGrupos")) )
	row += 1
	imp_linea_vacia(book, sheet, row, col, final=False, condiciones=True)
	row += 1

	for condicion in CONDIC_PRESUP:

		sheet.set_row(row, condicion.get("altura")) if condicion.get("altura") else None

		if condicion.get("columnas") == 1:
			sheet.write(row, col, condicion.get("contenido"), book.add_format(FORMATOS.get(condicion.get("formato"))))
			col += 1
		else:
			sheet.merge_range(row, col, row, col+condicion.get("columnas")-1, condicion.get("contenido"), book.add_format(FORMATOS.get(condicion.get("formato"))))
			col = 2
			row += 1
			imp_linea_vacia(book, sheet, row, col, final=False, condiciones=True)
			row += 1

	## print linea en blanco
	row -= 1
	imp_linea_vacia(book, sheet, row, col, final=True, condiciones=True)

	#row += 1


def crea_excel_presupuesto(queryset):
	'''
		Crea excel de un presupuesto. Se llama desde la acción "Crea Excel" de presupuestos_list 
	'''

	#queryset = queryset[0]
	for obj in queryset[:1]:
		
		_fileName = "P{}_{}_{}.xlsx".format(obj.id, re.sub(' ', '', obj.cliente.nombre.title()), re.sub(' ', '', obj.asunto.title()))

		response = HttpResponse(content_type='application/application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', charset='iso-8859-1')
		response['Content-Disposition'] = 'attachment; filename={}'.format(_fileName)

		book = Workbook(response)
		sheet = book.add_worksheet('Grupo SPEC')

		################# ANCHO Y ALTO #################
		format_filas_columnas(sheet)

		################# CABECERAS #################
		#row = 0
		row = imp_cabeceras(book, sheet, obj, "Soporte Grupo SPEC")

	row += 2
	col = 2

	################# ASUNTO #################
	sheet.merge_range(row, col, row, col+7, obj.asunto.title(), book.add_format(FORMATOS.get("headerGrupos")) )
	
	row += 2
	col = 2

	################# TITULOS COLUMNAS VACIA #################
	#titulos de grupos
	#valor y columnas que ocupa
	var_columnas = (("CÓDIGO",1), ("CANTIDAD",1), ("DESCRIPCIÓN",1), ("PRECIO UNITARIO",2), ("TOTAL",3),)

	for var, posic in var_columnas:
		if posic == 1:
			#sheet.write(row, col, var, book.add_format(dict(**FORMATOS.get("center"), **FORMATOS.get("medio"))))
			sheet.write(row, col, var, book.add_format(FORMATOS.get("headerGrupos")))
		else:
			#sheet.merge_range(row, col, row, col+posic-1, var, book.add_format(dict(**FORMATOS.get("center"), **FORMATOS.get("wrap"), **FORMATOS.get("medio"))))
			sheet.merge_range(row, col, row, col+posic-1, var, book.add_format(FORMATOS.get("headerGrupos")))

		col += posic
	################# FIN TITULOS COLUMNAS VACIA #################

	################# LINEA VACIA #################
	col = 2
	row += 1
	imp_linea_vacia(book, sheet, row, col)

	################# ITEMS #################
	row += 1
	lineas = LineaPresupuesto.objects.filter(presupuesto=obj.id)#.order_by('-check_in')
	initialRow = row

	#imprimiendo valores...
	for obj in queryset:
		for linea in lineas:
			sheet.write(row, col, linea.repuesto.codigo, book.add_format(FORMATOS.get("item_BI")) )
			sheet.write(row, col+1, linea.cantidad, book.add_format(FORMATOS.get("item_BI")))
			sheet.write(row, col+2, linea.repuesto.nombre, book.add_format(FORMATOS.get("item_BI")))	#descripcion
			sheet.write(row, col+3, obj.moneda.codigo, book.add_format(FORMATOS.get("item_BI")))
			sheet.write(row, col+4, linea.costo_custom if linea.costo_custom else linea.repuesto.costo * obj.tasa_cambio, book.add_format(FORMATOS.get("item_SB")))
			sheet.write(row, col+5, obj.moneda.codigo, book.add_format(FORMATOS.get("item_BI")))
			sheet.write_formula(row, col+6, "D{}*G{}".format(row+1, row+1), book.add_format(FORMATOS.get("item_SB")))
			sheet.write(row, col+7,"+ IVA", book.add_format(FORMATOS.get("item_BD")))

			row += 1
	################# FIN ITEMS #################
	
	################# LINEA VACIA #################
	imp_linea_vacia(book, sheet, row, col)
	
	################# LINEA TOTAL #################
	row += 1
	imp_linea_total(book, sheet, row, col, obj.moneda.codigo, initialRow, len(lineas))
	
	################# LINEA FINAL #################
	row += 1
	imp_linea_vacia(book, sheet, row, col, final=True)

	################# CONDICIONES COMERCIALES #################
	row += 2
	col = 2
	imp_condiciones(book, sheet, row, col, tipo="presupuesto")

	book.close()
	return response