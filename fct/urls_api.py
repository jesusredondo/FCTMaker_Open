from django.conf.urls import url

from fct.api import views_api_empresas


urlpatterns = [
    url(r'^empresas/(?P<curso_id>[0-9]*)$', views_api_empresas.empresas_json), #Supervisar como tutor

]