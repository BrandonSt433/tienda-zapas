from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.signup, name='registro'),
    path('iniciar_sesion/', views.signin, name='iniciar_sesion'),
    path('cerrar_sesion/', views.cerrarSesion, name='cerrar_sesion'),
]
