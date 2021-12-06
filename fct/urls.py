from django.conf.urls import url, include


from . import views


urlpatterns = [


    #Historico
    url(r'^historico/(?P<historico_id>[0-9]+)/$',views.historico_detalles, name='detalles_historico') ,

    url(r'^alumno/(?P<alumno_id>[0-9]+)/$',views.alumno_detalles, name='detalles_alumno') ,
    #Anexos
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo1/$', views.historico_anexo1, name='anexo1') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo2/$', views.historico_anexo2, name='anexo2') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo3/$', views.historico_anexo3, name='anexo3') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo4/$', views.historico_anexo4, name='anexo4') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo5/$', views.historico_anexo5, name='anexo5') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/anexo10B/$', views.historico_anexo10B, name='anexo6') ,
    url(r'^historico/(?P<historico_id>[0-9]+)/completo/$', views.historico_completo, name='completo') ,

    #Empresa
    url(r'^empresas/$', views.empresas_info, name='detalles_todas_empresas') ,
    url(r'^empresa/(?P<empresa_id>[0-9]+)/$', views.empresa_detalles, name='detalles_empresa') ,
    url(r'^empresa/(?P<empresa_id>[0-9]+)/anexo0/$', views.empresa_anexo0, name='anexo0') ,

    #index
    url(r'^$', views.index, name='index')

]

