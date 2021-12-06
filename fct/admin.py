# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Datos_Empresa, Tutor_Centro, Alumno, Ciclo_Formativo, Curso, Datos_Instituto,  Historico_Alumno_Curso

admin.site.register(Datos_Instituto)
admin.site.register(Tutor_Centro)
admin.site.register(Curso)
admin.site.register(Ciclo_Formativo)


class DatosEmpresaAdmin(admin.ModelAdmin):
    search_fields = ("nombre_empresa",)
admin.site.register(Datos_Empresa,DatosEmpresaAdmin)

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("getNombreCompleto",)
    #ordering = ('-nombre_alumno')  # The negative sign indicate descendent order

    def getNombreCompleto(self,obj):
        return obj.nombre_alumno+" "+obj.apellidos_alumno
    getNombreCompleto.short_description = 'Nombre Completo'
    getNombreCompleto.admin_order_field = 'nombre_alumno'

admin.site.register(Alumno, AlumnoAdmin)


#Otros:

@admin.register(Historico_Alumno_Curso)
class Historico_Alumno_Curso_Admin(admin.ModelAdmin):
    list_display = ( "getNombreCompleto", "getCiclo", "getCurso", "getEmpresa" )
    #, )

    def getNombreCompleto(self, obj):
        return obj.alumno
    getNombreCompleto.short_description = 'Nombre Completo'
    getNombreCompleto.admin_order_field = 'alumno__nombre_alumno'

    def getCiclo(self, obj):
        return obj.curso.ciclo_formativo.siglas_ciclo_formativo
    getCiclo.short_description = 'Ciclo'
    getCiclo.admin_order_field = 'curso__ciclo_formativo__siglas_ciclo_formativo'

    def getCurso(self, obj):
        return obj.curso.curso_academico
    getCurso.short_description = 'Curso'
    getCurso.admin_order_field = 'curso__curso_academico'

    def getEmpresa(self, obj):
        return obj.empresa
    getEmpresa.short_description = 'Empresa'
    getEmpresa.admin_order_field = 'empresa__nombre_empresa'




