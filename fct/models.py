# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models

from model_utils import Choices

from django.utils.timezone import now



# Create your models here.

@python_2_unicode_compatible
class Tutor_Centro(models.Model):
    nombre_tutor_centro = models.CharField(max_length=200)
    apellidos_tutor_centro = models.CharField(max_length=200)
    correo_tutor_centro = models.CharField(max_length=250, default='')
    def __str__(self):
        return self.nombre_tutor_centro+" "+self.apellidos_tutor_centro


@python_2_unicode_compatible
class Datos_Instituto(models.Model):
    nombre_director = models.CharField(max_length=200)
    apellidos_director = models.CharField(max_length=200)
    dni_director = models.CharField(max_length=20)
    nombre_instituto = models.CharField(max_length=100)
    codigo_instituto = models.CharField(max_length=20)
    localidad_instituto = models.CharField(max_length=20)
    provincia_instituto = models.CharField(max_length=20)
    calle_instituto = models.CharField(max_length=200)
    cod_postal_instituto = models.CharField(max_length=10)
    cif_instituto = models.CharField(max_length=20)
    telefono_instituto = models.CharField(max_length=15)
    fax_instituto = models.CharField(max_length=15)
    correo_instituto = models.CharField(max_length=300)
    def __str__(self):
        return self.nombre_instituto


@python_2_unicode_compatible
class Datos_Empresa(models.Model):
    numero_convenio = models.CharField(max_length=200)
    fecha_convenio =  models.DateField('Fecha firma convenio', default=now, blank=True )
    nombre_representante = models.CharField(max_length=200)
    apellidos_representante = models.CharField(max_length=200)
    nombre_tutor_empresa = models.CharField(max_length=200)
    apellidos_tutor_empresa = models.CharField(max_length=200)
    dni_representante = models.CharField(max_length=20)
    nombre_empresa = models.CharField(max_length=200)
    localidad_empresa = models.CharField(max_length=200)
    provincia_empresa = models.CharField(max_length=200)
    calle_empresa = models.CharField(max_length=250)
    cod_postal_empresa = models.CharField(max_length=200)
    cif_empresa = models.CharField(max_length=50)
    telefono_empresa = models.CharField(max_length=50)
    fax_empresa = models.CharField(max_length=50)
    correo_empresa = models.CharField(max_length=200)
    horario_empresa = models.CharField(max_length=250, default='No hay información disponible')
    def __str__(self):
        return self.nombre_empresa

@python_2_unicode_compatible
class Ciclo_Formativo(models.Model):
    nombre_ciclo_formativo = models.CharField(max_length=200)
    CICLOS = Choices("ASIR", "DAM", "DAW","SMR","SMRV", "FPB_IO_1", "FPB_IO_2")
    siglas_ciclo_formativo = models.CharField(choices=CICLOS, default=CICLOS.ASIR, max_length=20)
    clave_ciclo_formativo = models.CharField(max_length=20)
    def __str__(self):
        return self.nombre_ciclo_formativo

@python_2_unicode_compatible
class Curso(models.Model):
    curso_academico = models.CharField(max_length=50) #2017 - 2018
    inicio_realizacion_fct = models.DateField('Inicio de FCT')
    fin_realizacion_fct = models.DateField('Fin de FCT')
    horas_totales_fct = models.CharField(max_length=10,default='400')
    ciclo_formativo = models.ForeignKey(Ciclo_Formativo,null=True, on_delete=models.SET_NULL)
    tutor_centro = models.ForeignKey(Tutor_Centro,null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.curso_academico + " (" + self.mesesLetras() + ") - " + self.ciclo_formativo.nombre_ciclo_formativo + " - " + str(self.tutor_centro)
    def anioYNombre(self):
        return self.curso_academico + " - " + self.ciclo_formativo.nombre_ciclo_formativo
    def mesesLetras(self):
        return  "Marzo - Junio" if self.inicio_realizacion_fct.month < 7 else "Septiembre - Diciembre"
    def anioMesesCiclo(self):
        return self.curso_academico + " ("+ self.mesesLetras()+ ") - " + self.ciclo_formativo.nombre_ciclo_formativo
    def cursoMesesNombre(self):
        return self.curso_academico + (" ( Marzo-Junio ) " if self.inicio_realizacion_fct.month < 7 else " ( Septiembre-Diciembre ) ") + self.ciclo_formativo.nombre_ciclo_formativo


@python_2_unicode_compatible
class Alumno(models.Model):
    nombre_alumno = models.CharField(max_length=200)
    apellidos_alumno = models.CharField(max_length=200)
    dni_alumno = models.CharField(max_length=20)
    correo_alumno = models.CharField(max_length=60)
    def __str__(self):
        return self.nombre_alumno+" "+self.apellidos_alumno
    def matchNombreApellidos(nombre,apellidos):
        return Alumno.objects.filter(nombre_alumno__icontains=nombre, apellidos_alumno__icontains=apellidos)
    def matchCorreo(correo):
        return Alumno.objects.filter(correo_alumno__icontains=correo)
    def matchTCorreo_NombreApellidos(correo, nombre, apellidos):
        if Alumno.matchCorreo(correo):
            return Alumno.matchCorreo(correo)
        else :
            return Alumno.matchNombreApellidos(nombre, apellidos)


@python_2_unicode_compatible
class Historico_Alumno_Curso(models.Model):
    alumno = models.ForeignKey(Alumno,null=True, on_delete=models.PROTECT)
    curso = models.ForeignKey(Curso,null=True, on_delete=models.PROTECT)
    empresa = models.ForeignKey(Datos_Empresa,null=True, on_delete=models.PROTECT)
    def __str__(self):
        return self.alumno.nombre_alumno + " " + self.alumno.apellidos_alumno + " - " + self.curso.ciclo_formativo.siglas_ciclo_formativo + " - " + self.curso.curso_academico