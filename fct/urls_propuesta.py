from django.conf.urls import url

from fct.vistas import views_propuestas


urlpatterns = [
    url(r'^$',views_propuestas.propuesta) ,
    url(r'^proyecto/(?P<proyecto_id>[0-9]+)/supervisar$', views_propuestas.supervisar_proyecto), #Supervisar como tutor
    url(r'^proyecto/ver/(?P<proyecto_id>[0-9]+)$', views_propuestas.un_proyecto_ver),
    url(r'^proyecto/(?P<historico_id>[0-9]+)$',views_propuestas.proyecto) , #Nuevo/Editar. EL PARÁMETRO ES EL ID DEL HISTÓRICO!!!
    url(r'^proyecto_confirmacion$',views_propuestas.confirmar_proyecto), #Cuando enviamos el formulario para modificar/crear la propuesta.
    url(r'^proyecto_gestion$',views_propuestas.proyecto_gestion), #Donde vemos las distintas propuestas de distintos cursos y modificamos su estado.
    url(r'^proyecto/(?P<proyecto_id>[0-9]+)/descargarPDF$', views_propuestas.descargar_PDF), #Descarga el proyecto en cuestión como PDF.
]