    # -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse


#Directories:
import os
import shutil
import re


#Utilidades:
from fct.utilidades import removeNotAscii



from fct.models import Alumno, Curso, Tutor_Centro, Historico_Alumno_Curso, Datos_Empresa
from django.http import JsonResponse



###############
#API EMPRESAS:
###############

#Obtener todas las empresas en JSON:

def empresas_json(request,curso_id):
    if not request.user.is_superuser :
        return JsonResponse({'error':'HTTP 401'}, status=401)

    empresasJSON = []
    empresas = Datos_Empresa.objects.all().values()
    #Recorremos las empresas para gestionar el JSON de cada una de ellas:
    for empresa in empresas:
        empresaJSON = {'empresa': empresa}

        #Sacamos los cursos en los que participa la empresa:
        cursosEmpresaJSON = Curso.objects.filter(historico_alumno_curso__empresa_id=empresa['id']).distinct()
        empresaJSON['cursos'] = list(reversed(cursosEmpresaJSON.values()))


        #Sacamos los alumnos de FPB1 para la empresa:
        numAlumnosFPB1JSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'], historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='FPB_IO_1').count()
        empresaJSON['FPB_IO_1'] = numAlumnosFPB1JSON

        # Sacamos los alumnos de FPB2 para la empresa:
        numAlumnosFPB2JSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'], historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='FPB_IO_2').count()
        empresaJSON['FPB_IO_2'] = numAlumnosFPB2JSON

        # Sacamos los alumnos de SMR2 para la empresa:
        numAlumnosSMRJSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'],
                                                   historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='SMR').count()
        numAlumnosSMRJSON += Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'],
                                                  historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='SMRV').count()
        empresaJSON['SMR'] = numAlumnosSMRJSON

        # Sacamos los alumnos de ASIR2 para la empresa:
        numAlumnosASIRJSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'],
                                                  historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='ASIR').count()
        empresaJSON['ASIR'] = numAlumnosASIRJSON

        # Sacamos los alumnos de DAM2 para la empresa:
        numAlumnosDAMJSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'],
                                                  historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='DAM').count()
        empresaJSON['DAM'] = numAlumnosDAMJSON

        # Sacamos los alumnos de DAW2 para la empresa:
        numAlumnosDAWJSON = Alumno.objects.filter(historico_alumno_curso__empresa_id=empresa['id'],
                                                  historico_alumno_curso__curso__ciclo_formativo__siglas_ciclo_formativo='DAW').count()
        empresaJSON['DAW'] = numAlumnosDAWJSON


        #Añadimos la empresa en JSON
        empresasJSON.append(empresaJSON)

    return JsonResponse(empresasJSON,safe=False)

