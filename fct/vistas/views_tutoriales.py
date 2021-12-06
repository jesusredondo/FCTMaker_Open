# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.http import HttpResponse


def tutoriales(request):
    if(request.user.is_superuser):
        return redirect('/tutoriales/profesores')
    else:
        return redirect('/')


def profesores(request):
    return render(request, 'fct/tutoriales/profesores/profesores.html')#,context)

