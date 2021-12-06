"""FCTMaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views
from fct.views import home



#Markdown:


#No cache for static files:
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache


#Django-Rest:



#Router para la API REST
#TODO: Descomentar cuando se retome lo del QR:
#router = routers.DefaultRouter()
#router.register(r'users', views_rest.UserViewSet)
#router.register(r'groups', views_rest.GroupViewSet)
#router.register(r'datos_empresas', views_rest.DatosEmpresaViewSet)

urlpatterns = [

    #static
    url(r'^static/(?P<path>.*)$', never_cache(serve_static)),
    url(r'^fct/', include('fct.urls')),
    url(r'^admin/', admin.site.urls, name='admin'),
    #url(r'^propuesta/',include('fct.urls_propuesta')),
    #url(r'^upload/',include('fct.urls_upload')),    #TODO: POR AHORA, DESACTIVADO
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    #url(r'^markdownx/', include(markdownx)),
    #url(r'^superadmin/',include(('fct.superadmin.urls_superadmin'))),
    url(r'^ajax/',include('fct.ajax.urls_ajax')),
    #url(r'^proyectos/',include('fct.proyectos.urls_proyectos')),
    url(r'^tutoriales/',include('fct.urls_tutoriales')),
    url(r'^api/',include('fct.urls_api')),
    #url(r'^pruebas/',include('fct.urls_pruebas')),
    #Django-Rest Authentication:
    #De momento comentado, descomentar cuando se retome.
    #path('api-rest/', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls')),
    #path('api-token-auth/', obtain_auth_token),


    url(r'^$', home, name='home'),
]
