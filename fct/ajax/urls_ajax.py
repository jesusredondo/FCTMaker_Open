from django.conf.urls import url

from fct.ajax import views_ajax


urlpatterns = [
    #Alumnos FCT
    url(r'getCursosTutorID',views_ajax.cursos_tutor, name='ajax_get_cursos_tutorID'),
    url(r'getAlumnosCursoID',views_ajax.alumnos_curso, name='ajax_get_alumnos_cursoID'),
    #Tutoriales:
    url(r'getTutorialProfesor/(?P<nombre_tutorial>\w+)/$',views_ajax.tutoriales_get_tutorial_profesor, name='ajax_get_tutorial_tutorialNombre'),
]