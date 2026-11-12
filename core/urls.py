from django.urls import path

from . import views

urlpatterns = [
    path("", views.pagina_inicial, name="home"),
    path("conteudo/<slug:slug>/", views.exibir_conteudo, name="conteudo"),
]
