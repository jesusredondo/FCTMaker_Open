# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Datos_Empresa, Tutor_Centro, Alumno, Curso, Datos_Instituto, Historico_Alumno_Curso

#Genera un contexto a partir del ID de un alumno.
def generar_contexto_historico(historico_id):
    datos_instituto = Datos_Instituto.objects.first()
    historico = get_object_or_404(Historico_Alumno_Curso, pk=historico_id )
    alumno = get_object_or_404(Alumno, pk=historico.alumno_id)
    datos_empresa = historico.empresa
    curso = historico.curso
    tutor_centro = historico.curso.tutor_centro

    context = {
        #Datos_Instituto
        'nombre_director': datos_instituto.nombre_director,
        'apellidos_director': datos_instituto.apellidos_director,
        'dni_director': datos_instituto.dni_director,
        'nombre_instituto': datos_instituto.nombre_instituto,
        'codigo_instituto': datos_instituto.codigo_instituto,
        'localidad_instituto': datos_instituto.localidad_instituto,
        'provincia_instituto': datos_instituto.provincia_instituto,
        'calle_instituto': datos_instituto.calle_instituto,
        'cod_postal_instituto': datos_instituto.cod_postal_instituto,
        'cif_instituto': datos_instituto.cif_instituto,
        'telefono_instituto': datos_instituto.telefono_instituto,
        'fax_instituto': datos_instituto.fax_instituto,
        'correo_instituto': datos_instituto.correo_instituto,

        #Datos_Empresa
        'numero_convenio' : datos_empresa.numero_convenio,
        'fecha_convenio' : datos_empresa.fecha_convenio,
        'nombre_tutor_empresa': datos_empresa.nombre_tutor_empresa,
        'apellidos_tutor_empresa': datos_empresa.apellidos_tutor_empresa,
        'nombre_representante': datos_empresa.nombre_representante,
        'apellidos_representante': datos_empresa.apellidos_representante,
        'dni_representante': datos_empresa.dni_representante,
        'nombre_empresa': datos_empresa.nombre_empresa,
        'localidad_empresa': datos_empresa.localidad_empresa,
        'provincia_empresa': datos_empresa.provincia_empresa,
        'calle_empresa': datos_empresa.calle_empresa,
        'cod_postal_empresa': datos_empresa.cod_postal_empresa,
        'cif_empresa': datos_empresa.cif_empresa,
        'telefono_empresa': datos_empresa.telefono_empresa,
        'fax_empresa': datos_empresa.fax_empresa,
        'correo_empresa': datos_empresa.correo_empresa,
        'horario_empresa' : datos_empresa.horario_empresa,

        #Tutor_Centro
        'nombre_tutor_centro' : tutor_centro.nombre_tutor_centro,
        'apellidos_tutor_centro' : tutor_centro.apellidos_tutor_centro ,
        'correo_tutor_centro' : tutor_centro.correo_tutor_centro ,

        #Curso
        'nombre_ciclo_formativo': curso.ciclo_formativo.nombre_ciclo_formativo,
        'siglas_ciclo_formativo': curso.ciclo_formativo.siglas_ciclo_formativo,
        'clave_ciclo_formativo': curso.ciclo_formativo.clave_ciclo_formativo,
        'curso_academico': curso.curso_academico,
        'inicio_realizacion_fct': curso.inicio_realizacion_fct,
        'fin_realizacion_fct': curso.fin_realizacion_fct,
        'inicio_realizacion_fct_mes': diccionarioMeses[curso.inicio_realizacion_fct.month],
        'fin_realizacion_fct_mes': diccionarioMeses[curso.fin_realizacion_fct.month],
        'horas_totales_fct': curso.horas_totales_fct,

        #Alumno
        'nombre_alumno' : alumno.nombre_alumno ,
        'apellidos_alumno' : alumno.apellidos_alumno ,
        'dni_alumno' : alumno.dni_alumno,
        'correo_alumno' : alumno.correo_alumno,


        #Otros
        'dia_hoy': timezone.now().day,
        'mes_hoy': timezone.now().month,
        'mes_hoy_letras': diccionarioMeses[timezone.now().month],
        'anio_hoy': timezone.now().year,
        'anio_anterior': timezone.now().year - 1,




    }


#Gestionar si hay varios alumnos para anexo 1:
    historicos_anexo_1 = historico.curso.historico_alumno_curso_set.filter(empresa__pk=datos_empresa.pk)
    for tupla_historico_extra in enumerate(historicos_anexo_1) :
        context['nombre_alumno_' + str(tupla_historico_extra[0]+1)] = tupla_historico_extra[1].alumno.nombre_alumno
        context['apellidos_alumno_' + str(tupla_historico_extra[0]+1)] = tupla_historico_extra[1].alumno.apellidos_alumno
        context['dni_alumno_' + str(tupla_historico_extra[0]+1)] = tupla_historico_extra[1].alumno.dni_alumno




    return context


# Genera contexto para el Anexo 0.
def generar_contexto_anexo_0(empresa_id):
    datos_instituto = Datos_Instituto.objects.first()
    datos_empresa =  get_object_or_404(Datos_Empresa, pk=empresa_id)
    context = {
        # Datos_Instituto
        'nombre_director': datos_instituto.nombre_director,
        'apellidos_director': datos_instituto.apellidos_director,
        'dni_director': datos_instituto.dni_director,
        'nombre_instituto': datos_instituto.nombre_instituto,
        'codigo_instituto': datos_instituto.codigo_instituto,
        'localidad_instituto': datos_instituto.localidad_instituto,
        'provincia_instituto': datos_instituto.provincia_instituto,
        'calle_instituto': datos_instituto.calle_instituto,
        'cod_postal_instituto': datos_instituto.cod_postal_instituto,
        'cif_instituto': datos_instituto.cif_instituto,
        'telefono_instituto': datos_instituto.telefono_instituto,
        'fax_instituto': datos_instituto.fax_instituto,
        'correo_instituto': datos_instituto.correo_instituto,

        # Datos_Empresa
        'numero_convenio': datos_empresa.numero_convenio,
        'fecha_convenio': datos_empresa.fecha_convenio,
        'nombre_tutor_empresa': datos_empresa.nombre_tutor_empresa,
        'apellidos_tutor_empresa': datos_empresa.apellidos_tutor_empresa,
        'nombre_representante': datos_empresa.nombre_representante,
        'apellidos_representante': datos_empresa.apellidos_representante,
        'dni_representante': datos_empresa.dni_representante,
        'nombre_empresa': datos_empresa.nombre_empresa,
        'localidad_empresa': datos_empresa.localidad_empresa,
        'provincia_empresa': datos_empresa.provincia_empresa,
        'calle_empresa': datos_empresa.calle_empresa,
        'cod_postal_empresa': datos_empresa.cod_postal_empresa,
        'cif_empresa': datos_empresa.cif_empresa,
        'telefono_empresa': datos_empresa.telefono_empresa,
        'fax_empresa': datos_empresa.fax_empresa,
        'correo_empresa': datos_empresa.correo_empresa,
        'horario_empresa': datos_empresa.horario_empresa,



        # Otros
        'dia_hoy': timezone.now().day,
        'mes_hoy': timezone.now().month,
        'mes_hoy_letras': diccionarioMeses[timezone.now().month],
        'anio_hoy': timezone.now().year,
        'anio_anterior': timezone.now().year - 1,
    }
    return context

















#Metodos para parsear los alumnos:
def generar_students():
    columnHeightTitles = 0
    alumnoColumn = 0
    grupoColumn = 0
    dniColumn = 0
    students = []

    # Load:
    workbook = xlrd.open_workbook('fct/temporales/xlsTemporal.xls')
    sheet = workbook.sheet_by_index(0)

    # Working with the sheet:

    # First we locate where the "Alumno title cell is"
    cellValue = sheet.cell(columnHeightTitles, alumnoColumn).value
    while (cellValue.lower() != 'alumno'):
        columnHeightTitles += 1
        cellValue = sheet.cell(columnHeightTitles, alumnoColumn).value

    # Then we locate the "Grupo" and "D.N.I." columns
    column = 0
    while (column < sheet.ncols):
        cellValue = sheet.cell(columnHeightTitles, column).value
        if (cellValue.lower() == 'grupo'):
            grupoColumn = column
        if (cellValue.lower() == "d.n.i."):
            dniColumn = column
        column += 1

    # TODO: Error control when not grupoColumn or dniColumn

    # Dictinoary creation:
    row = columnHeightTitles + 1
    i = 0
    while (row < sheet.nrows):
        students.append({
            'nombre_alumno': sheet.cell(row, alumnoColumn).value.split(',')[1].encode('utf-8'),
            'apellidos_alumno': sheet.cell(row, alumnoColumn).value.split(',')[0].encode('utf-8'),
            'dni_alumno': sheet.cell(row, dniColumn).value.encode('utf-8'),
            'curso__siglas_ciclo_formativo': sheet.cell(row, grupoColumn).value[:-1].encode('utf-8'),
        })
        row += 1
    return students



diccionarioNoAscii = {"á":"a",
                      "à":"a",
                      "â":"a",
                      "Á":"A",
                      "À":"A",
                      "Â":"A",
                      #E
                      "é": "e",
                      "è": "e",
                      "è": "e",
                      "É": "E",
                      "È": "E",
                      "Ê": "E",
                      #I
                      "í": "i",
                      "ì": "i",
                      "î": "i",
                      "Í": "I",
                      "Ì": "I",
                      "Î": "I",
                      #O
                      "ó": "o",
                      "ò": "o",
                      "ô": "o",
                      "Ó": "O",
                      "Ò": "O",
                      "Ô": "O",
                      #U
                      "ú": "u",
                      "ù": "u",
                      "û": "u",
                      "ü": "U",
                      "Ú": "U",
                      "Ü": "U",
                      #Ñ
                      "ñ":"n",
                      "Ñ":"N",
                      #Ç
                      "ç":"c",
                      "Ç":"C",
                      #ESPACIO
                      " ":"_",
                      #COMAS
                      ",":"_"

                          }

#Método para eliminar todo lo que no pueda ser ascii:
def removeNotAscii (cadena):
    #print (cadena)
    #cadena = cadena.encode('utf-8')
    for key,value in diccionarioNoAscii.items():
        #print "\t"+key+" --- "+ value
        cadena = cadena.replace(key,value)
    #print (cadena)
    return cadena


#Correspondencia Meses:
diccionarioMeses = {
    1: 'Enero',
    2: 'Febrero',
    3: 'Marzo',
    4: 'Abril',
    5: 'Mayo',
    6: 'Junio',
    7: 'Julio',
    8: 'Agosto',
    9: 'Septiembre',
    10: 'Octubre',
    11: 'Noviembre',
    12: 'Diciembre'
}






#Método para generar los periodos desde hoy hasta el inicio del servicio (2018-2019).
def generarPeriodosDesdeInicio():
    periodos = [] # Guarda una tupla con el nombre del periodo y una fecha central para realizar las búsquedas.
    hoy = timezone.now()
    fechaRefIntermedia = timezone.now()
    if hoy.month >= 8:  # Ya tiene sentido ir pensando en el periodo del curso añoactual/añosiguiente
        fechaRefIntermedia = fechaRefIntermedia.replace(month=5, day=1, year=fechaRefIntermedia.year+1)
        periodos.append([f"{hoy.year} / {hoy.year+1} - Marzo - Junio ", fechaRefIntermedia])

    if hoy.month >= 5:  # En mayo ya añadimos el periodo de Diciembre extraoridinario del añoanterior/añoactual
        fechaRefIntermedia = fechaRefIntermedia.replace(month=11, day=1, year=hoy.year)
        periodos.append([f"{hoy.year - 1} / {hoy.year} - Septiembre - Diciembre (Extraordinario)", fechaRefIntermedia])



    #El junio del año en el que estamos (añoanterior/añoactual)
    fechaRefIntermedia = fechaRefIntermedia.replace(month=5, day=1, year=hoy.year)
    periodos.append([f"{hoy.year - 1} / {hoy.year} - Marzo - junio", fechaRefIntermedia])

    #Seguimos metiendo periodos, dos por año: añoanterior/añoactual, primero Diciembre y luego Junio.
    anioReferencia = hoy.year - 1
    while( anioReferencia > 2018) :
        #Extraordinaria
        fechaRefIntermedia = fechaRefIntermedia.replace(month=11, day=1, year=anioReferencia)
        periodos.append([f"{anioReferencia - 1} / {anioReferencia} - Septiembre - Diciembre (Extraordinario)", fechaRefIntermedia])
        #Ordinaria
        fechaRefIntermedia = fechaRefIntermedia.replace(month=5, day=1, year=anioReferencia)
        periodos.append([f"{anioReferencia - 1} / {anioReferencia} - Marzo - Junio ", fechaRefIntermedia])
        anioReferencia -= 1

    return periodos


#MENSAJE PARA DEPURAR.
def depurarMsg(contenido, titulo="-------"):
    print("\n-"+titulo+"---\n\n");
    print(contenido)
    print("\n-----------\n\n");