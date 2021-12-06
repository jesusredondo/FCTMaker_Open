from django.conf.urls import url

from fct.vistas import views_tutoriales


urlpatterns = [
    url(r'^$',views_tutoriales.tutoriales) , #Redireccionar tutorial a alumno o profesor
    url(r'^profesores$', views_tutoriales.profesores) # Muestra el index de tutoriales para profesores.
]