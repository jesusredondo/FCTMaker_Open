# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404


# Create your views here.
from ..models import Curso, Historico_Alumno_Curso

from django.shortcuts import render, get_object_or_404, redirect, Http404


#########
#FRAGMENTOS AJAX:
#########

#Cargar los cursos de un profesor ordenados de moderno a antiguo:
def cursos_tutor(request):
    tutorID = request.GET.get('tutorID')
    cursos  = Curso.objects.filter(tutor_centro_id=tutorID).order_by('-inicio_realizacion_fct') #El - antes para hacerlo descendente
    return render(request, 'fct/AJAXSnippet/getCursosTutorID.html', {'cursos': cursos})


#Cargar los cursos de un profesor ordenados de moderno a antiguo:
def alumnos_curso(request):
    cursoID = request.GET.get('cursoID')
    alumnosHistorico  = Historico_Alumno_Curso.objects.filter(curso_id=cursoID)
    return render(request, 'fct/AJAXSnippet/getAlumnosCursoID.html', {'alumnosHistorico': alumnosHistorico})




##############
# TUTORIALES:
##############

def tutoriales_get_tutorial_profesor(request, nombre_tutorial) :
    if request.user.is_superuser :
        return render(request,'fct/tutoriales/profesores/'+nombre_tutorial+'.html')
    else :
        return redirect('/')