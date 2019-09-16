#2: Linea gruesa. 6: Doble raya
BORDER_STYLE = 2

FORMATOS = {
    ### TEXTO ##
    "negrita" : {"bold": True},
    "bg_gris" : {"bg_color": "#f2f2f2"},
    "segoe" : {"font_name": "Segoe UI"},
    "rojo" : {"font_color": "#ff0000"},

    ### FECHAS ###
    "fecha" : {"num_format": "dd/mm/yyyy"},

    "fechaIzq" : {
        "num_format": "dd/mm/yyyy",
        "align": "left",
    },

    ### ALINEACION ###
    #Horizontal
    "izquierda" : {"align": "left"},
    "center" : {"align": "center"},
    "derecha" : {"align": "right"},
    #Vertical
    "medio" : {"valign": "vcenter"},

    ### CELDA ###
    "wrap" : {'text_wrap': True},
    "linea_inf" : {
        "bottom": BORDER_STYLE,
    },

    ### GRUPOS ###
    #headers keys
    "headerKeys" : {
        "bold": True,
        "align": "left",
    },
    #DE: bajo imagen
    "bajoImg": {
        "bold": True,
        "align": "right",
    },
    #cabeceras de grupos. No del doc.
    "headerGrupos" : {
        "bold": True,
        "align": "center",
        "text_wrap": True,
        "valign": "vcenter",
        "border": BORDER_STYLE,
        "bg_color": "#008080",
        "font_color": "white",
        "font_size": 10,
        "font_name": "Segoe UI Black",
    },

    #item borde izquierdo
    "item_BI" : {
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
        "left": BORDER_STYLE,
        "font_size": 10,
    },
    #item borde derecho
    "item_BD" : {
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
        "right": BORDER_STYLE,
        "font_size": 10,
    },
    #item sin borde
    "item_SB" : {
        "align": "center",
        "valign": "vcenter",
        "text_wrap": True,
        "font_size": 10,
    },

    #Condiciones comerciales
    "condic_key" : {
        "align": "left",
        "valign": "vcenter",
        "text_wrap": True,
        "left": BORDER_STYLE,
        "bold": True,
        "underline": 1,
        "font_size": 10,
    },
    "condic_value" : {
        "align": "left",
        "valign": "vcenter",
        "text_wrap": True,
        "right": BORDER_STYLE,
        "font_size": 10,
    },

}

CONDIC_OFERTAS = [
    {
        "contenido": "VALIDEZ DE LA OFERTA:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "15 días corridos.",
        "formato": "condic_value",
        "columnas": 7,
    },
    {
        "contenido": "FORMA DE PAGO:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "50% al pedido. \n50% a la entrega de equipos y software (a excepción de los servicios). \nSaldo de servicios contra finalización de la implementación (Go-Live).",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 42,
    },
    {
        "contenido": "GARANTIA:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "6 meses con opción a renovación anual de forma indefinida a través de la contratación del servicio de mantenimiento.\n*Molinetes y barreras: 6 meses.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 30,
    },
    {
        "contenido": "PRECIOS:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "Impuestos no incluidos. \nNo se incluye el envío de los productos. \nEn el caso de reparación de equipos, los mismos serán analizados y reparados según lo definido en la garantía/SLA.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 43,
    },
    {
        "contenido": "INSTALACIÓN:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "Se incluye la instalación física de los productos cotizados.\nEn las horas de consultoría, se incluyen la instalación remota, configuración y parametrización de la aplicación.\nNo se incluye cableado. En cada punto donde irá instalado cada uno de los terminales, se requiere contar con tomacorriente de 220VAC y cable/boca de red.\nTodos los servicios incluidos en la presente oferta serán realizados en el horario de 9 a 18 horas, días hábiles de lunes a viernes. Trabajos fuera de dichos horarios, serán cotizados en caso de ser necesarios.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 86,
    },
    {
        "contenido": "FACTURACIÓN:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "Todos los precios están expresados en Dólares USA. Deberán ser abonados en Dólares ó su equivalente en pesos de curso legal vigente según la cotización tipo vendedor en el mercado oficial, correspondiente al cierre del día de la acreditación de los fondos en el caso de entrega de cheques de pago diferido, o al cierre del día anterior a la fecha de pago de tratarse de cheques al día. A los efectos legales los precios serán indicados por unidad y expresados en pesos según la cotización del dólar libre tipo vendedor del día de emisión de la correspondiente factura. La diferencia de cambio surgida entre el día de la factura y el día de acreditación de los fondos generará una nota de débito/crédito por el importe respectivo.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 83.25,
    },
]

CONDIC_PRESUP = [
    {
        "contenido": "VALIDEZ DE LA OFERTA:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "7 días corridos.",
        "formato": "condic_value",
        "columnas": 7,
    },
    {
        "contenido": "IMPUESTOS:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "No incluidos.",
        "formato": "condic_value",
        "columnas": 7,
    },
    {
        "contenido": "PRECIOS:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "No incluyen flete, gastos de desplazamiento y/o estadía fuera de Capital Federal.\nTodos los servicios incluidos en la presente oferta serán realizados de Lunes a Viernes en el horario de  9 a 18 horas en días hábiles; trabajos fuera de estas condiciones, deberán solicitarse expresamente.\nEl valor mínimo de la visita técnica es el equivalente a 4 (cuatro) horas de consultoría. En caso de que el tiempo efectivo de servicio supere el tiempo estimado, se procederá a cobrar el excedente.\nPara poder realizar las tareas implicadas, será necesario contar con la OC o aceptación del presupuesto.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 83.25,
    },
    {
        "contenido": "FACTURACIÓN:",
        "formato": "condic_key",
        "columnas": 1,
    },
    {
        "contenido": "Todos los precios están expresados en Dólares USA. Deberán ser abonados en Dólares ó su equivalente en pesos de curso legal vigente según la cotización tipo vendedor en el mercado oficial, correspondiente al cierre del día de la acreditación de los fondos en el caso de entrega de cheques de pago diferido, o al cierre del día anterior a la fecha de pago de tratarse de cheques al día. A los efectos legales los precios serán indicados por unidad y expresados en pesos según la cotización del dólar libre tipo vendedor del día de emisión de la correspondiente factura. La diferencia de cambio surgida entre el día de la factura y el día de acreditación de los fondos generará una nota de débito/crédito por el importe respectivo.",
        "formato": "condic_value",
        "columnas": 7,
        "altura": 85.5,
    },
]
