# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError



from.utilidades import generar_contexto_historico, generar_contexto_anexo_0, removeNotAscii, generarPeriodosDesdeInicio, depurarMsg

#To work with Doc files:
from docxtpl import DocxTemplate

# Create your views here.
from .models import Datos_Empresa, Tutor_Centro, Alumno, Curso, Datos_Instituto, Historico_Alumno_Curso

#Directories:
import os
import shutil
import re

#Fetch JSON data:
import urllib.request, json, urllib.parse


#########
#HOME:
#########
def home(request):
    context = {}


    #Si llega un alumno, guardamos su referencia:
    if hasattr(request.user, 'email'):
        mitadEmail = request.user.email.split('@')[0] #No voy a discriminar si es el email largo o corto.

        if Alumno.objects.filter(correo_alumno__startswith=mitadEmail) :
            context['alumno'] = Alumno.objects.filter(correo_alumno__startswith=mitadEmail)[0]

    return render(request, 'home.html', context)



#########
#INDEX:
#########
def index(request):
    instituto = Datos_Instituto.objects.first()
    cursos = Curso.objects.all()
    context={'instituto':instituto ,
             'tutores':Tutor_Centro.objects.exclude(curso__isnull=True)}

    ##Creamos un diccionario que guarda lo siguiente:
    #Cada uno de los tutores del sistema, es la clave. El valor es una lista de dos elementos:
    # 1) El periodo (es una lista con [nombre periodo,  Fecha intermedia periodo] - Convertirlo para simplificar
    # 2) Una lista con los alumnos que hay para dicho periodo
#    tutores = Tutor_Centro.objects.all()
#    periodos = generarPeriodosDesdeInicio()


#    tutor_periodo_alumnos = {}
#    for tutor in tutores:
#        tutor_periodo_alumnos[tutor] = [periodos,[]]
#        cursos_de_profe = Curso.objects.filter(tutor_centro=tutor)



    return render(request, 'fct/index.html', context)









#########
#ALUMNOS:
#########

def alumno_detalles(request, alumno_id):
    alumno = get_object_or_404(Alumno, pk=alumno_id)
    context= {'alumno':alumno}
    return render(request, 'fct/alumno/detallesAlumno.html', context)





#########
#EMPRESAS:
#########

def empresas_info(request):
    context ={}
    return render(request, 'fct/empresa/empresas.html', context)



def empresa_detalles(request, empresa_id):
    empresa = get_object_or_404(Datos_Empresa, pk=empresa_id)
    historicos_de_empresa = Historico_Alumno_Curso.objects.filter(empresa__pk=empresa.id).order_by('curso__ciclo_formativo__siglas_ciclo_formativo', '-curso__inicio_realizacion_fct')

    # TODO: No sirve, borrar en próximas versiones
    #  #historicos_de_empresa = get_list_or_404(Historico_Alumno_Curso, empresa__pk=empresa.id)
    '''tieneASIR = [False,0] #Si it has and the id of one alumno of ASIR.
    tieneDAM = [False,0]
    tieneDAW = [False,0]
    tieneSMR = [False,0]'''

    '''for historico in historicos_de_empresa :
        if re.search("ASIR", historico.curso.ciclo_formativo.siglas_ciclo_formativo, re.IGNORECASE) :
            tieneASIR[0] = True;
            tieneASIR[1] = historico.id
        if re.search("DAM", historico.curso.ciclo_formativo.siglas_ciclo_formativo, re.IGNORECASE) :
            tieneDAM[0] = True;
            tieneASIR[1] = historico.id
        if re.search("DAW", historico.curso.ciclo_formativo.siglas_ciclo_formativo, re.IGNORECASE) :
            tieneDAW[0] = True;
            tieneASIR[1] = historico.id
        if re.search("SMR", historico.curso.ciclo_formativo.siglas_ciclo_formativo, re.IGNORECASE) :
            tieneSMR[0] = True;
            tieneASIR[1] = historico.id'''

    context = {'empresa': empresa,
               'historicos_de_empresa': historicos_de_empresa,}

                #'tieneASIR':tieneASIR,
                #'tieneDAM':tieneDAM,
                #'tieneDAW':tieneDAW,
                #'tieneSMR':tieneSMR}


    #Sacamos info de los alumnos de los últimos 6 cursos:
#    cursos_DAW = {}
    num_ultimos_cursos = 8

    #Actualiza el contexto con alumnos_ciclo.
    alumnos_ciclo = {}
    for siglas_curso in ["FPB_IO_1", "FPB_IO_2","SMR","SMRV","ASIR","DAM","DAW"]:
        total_alumnos_ciclo = 0
        alumnos_ciclo[siglas_curso] ={}
        cursos_ultimos = reversed(Curso.objects.filter(ciclo_formativo__siglas_ciclo_formativo=siglas_curso,historico_alumno_curso__empresa__id=empresa.id).order_by('-inicio_realizacion_fct').distinct()[:num_ultimos_cursos])
        alumnos_ciclo[siglas_curso]['alumn'] = []
        alumnos_ciclo[siglas_curso]['nombres_cursos'] = []
        for curso in cursos_ultimos:
            alumnos_ciclo[siglas_curso]['nombres_cursos'].append(curso.curso_academico +' '+ curso.mesesLetras())
            num_alumnos_curso = Historico_Alumno_Curso.objects.filter(curso__id=curso.id, empresa__id=empresa.id).count()
            alumnos_ciclo[siglas_curso]['alumn'].append(num_alumnos_curso)
            total_alumnos_ciclo += num_alumnos_curso
        #Si no hay ningún alumno en ese ciclo en esa empresa, lo eliminamos:
        if total_alumnos_ciclo == 0 :
            del alumnos_ciclo[siglas_curso]

    print(alumnos_ciclo)
    context['alumnos_ciclo']=alumnos_ciclo

    return render(request, 'fct/empresa/detallesEmpresa.html', context)



#########
#HISTORICO ALUMNOS:
#########

def historico_detalles(request, historico_id):
    historico = get_object_or_404(Historico_Alumno_Curso, pk=historico_id)
    context= {'historico':historico}
    return render(request, 'fct/historico/detallesHistorico.html', context)


def empresa_anexo0(request, empresa_id):
    context = generar_contexto_anexo_0(empresa_id)
    #Anexo 0 is different is is an ERASMUS student
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo0.docx")
    #if ("ERASMUS" in context['siglas_ciclo_formativo']):  ##EL ANEXO 0 va por otro lado.
    #    doc0 = DocxTemplate("fct/templatesDOCX/Anexo0_ERASMUS.docx")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_empresa'][:23]+'_anexo0.docx') #The name of the document includes the name of the enterprise and CCFF.
    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo1(request, historico_id):
    context = generar_contexto_historico(historico_id)
    # Anexo 1 is different is is an ERASMUS student
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo1.docx")
    if ("ERASMUS" in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo1_ERASMUS.docx")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_empresa'][:23]+'_'+context['siglas_ciclo_formativo']+'_anexo1.docx')
    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo2(request, historico_id):
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_DAM.docx")
    context = generar_contexto_historico(historico_id)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_alumno']+"_"+context['apellidos_alumno']+'_anexo2.docx')

    #Anexo base is different depending on the CCFF:
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 =  DocxTemplate("fct/templatesDOCX/Anexo2_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'DAW'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_DAW.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_FPB.docx")
    elif ("ERASMUS" in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_ERASMUS.docx")

    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo3(request, historico_id):
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_DAM.docx")
    context = generar_contexto_historico(historico_id)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_alumno']+"_"+context['apellidos_alumno']+'_anexo3.docx')

    # Anexo base is different depending on the CCFF:
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'DAW'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_DAW.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_FPB.docx")

    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo4(request, historico_id):
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_DAM.docx")
    context = generar_contexto_historico(historico_id)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_alumno']+"_"+context['apellidos_alumno']+'_anexo4.docx')

    # Anexo base is different depending on the CCFF:
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'DAW'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_DAW.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_FPB.docx")

    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo5(request, historico_id):
    context = generar_contexto_historico(historico_id)
    #Anexo 0 varies depending on erasmus
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo5.docx")
    if ("ERASMUS" in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo5_ERASMUS.docx")

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_alumno']+"_"+context['apellidos_alumno']+'_anexo5.docx')

    doc0.render(context)
    doc0.save(response)
    return response

def historico_anexo10B(request, historico_id):
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo10-B.docx")
    context = generar_contexto_historico(historico_id)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    response['Content-Disposition'] = 'attachment; filename='+removeNotAscii(context['nombre_alumno']+"_"+context['apellidos_alumno']+'_anexo10-B.docx')
    doc0.render(context)
    doc0.save(response)
    return response






def historico_completo(reques, historico_id):
    #TODO: Use vars for the paths. It will be hell rewrtting code in the future
    ###########################
    # Generate Anexos in disk #
    ###########################

    #Delete old files
    for zipFile in os.listdir('fct/temporales'):
        if zipFile.endswith('.zip'):
            os.remove(os.path.join('fct/temporales',zipFile))

    rutaAlumnoDisco = os.path.join("fct/temporales","alumno") #TODO: Por ahora siempre se queda en la carpeta alumno
    if (os.path.isdir(rutaAlumnoDisco)):
        shutil.rmtree(rutaAlumnoDisco)
    os.mkdir(rutaAlumnoDisco)

    #Generar Contexto:
    context = generar_contexto_historico(historico_id)

    #Anexo0:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo0.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco+"/",removeNotAscii(context['nombre_empresa'][:23] + '_anexo0.docx')))
    # Anexo1:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo1.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_empresa'][:23] + '_' + context[
        'siglas_ciclo_formativo'] + '_anexo1.docx')))
    # Anexo2:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_DAM.docx")
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'DAW'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_DAW.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo2_FPB.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_alumno'] + "_" + context[
        'apellidos_alumno'] + '_anexo2.docx')))
    # Anexo3:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_DAM.docx")
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'FPB'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_FPB.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo3_FPB.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_alumno'] + "_" + context[
        'apellidos_alumno'] + '_anexo3.docx')))
    # Anexo4:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_DAM.docx")
    if (context['siglas_ciclo_formativo'] == 'ASIR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_ASIR.docx")
    elif (context['siglas_ciclo_formativo'] == 'SMR'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_SMR.docx")
    elif (context['siglas_ciclo_formativo'] == 'DAW'):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_DAW.docx")
    elif ('FPB' in context['siglas_ciclo_formativo']):
        doc0 = DocxTemplate("fct/templatesDOCX/Anexo4_FPB.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_alumno'] + "_" + context[
        'apellidos_alumno'] + '_anexo4.docx')))
    # Anexo5:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo5.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_alumno'] + "_" + context[
        'apellidos_alumno'] + '_anexo5.docx')))
    # Anexo10B:
    doc0 = DocxTemplate("fct/templatesDOCX/Anexo10-B.docx")
    doc0.render(context)
    doc0.save(os.path.join(rutaAlumnoDisco + "/", removeNotAscii(context['nombre_alumno'] + "_" + context[
        'apellidos_alumno'] + '_anexo10-B.docx')))

    #Comprimirlos
    zipFilePath = removeNotAscii("fct/temporales/"+context['nombre_alumno']+"_"+context['apellidos_alumno']+"_"+context["dni_alumno"])
    shutil.make_archive(zipFilePath, 'zip', rutaAlumnoDisco)

    #Devolverlos
    zipFile = open(zipFilePath+".zip",'rb')
    response = HttpResponse(zipFile, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="'+(zipFilePath[:15]+".zip")+'"'
    return response














