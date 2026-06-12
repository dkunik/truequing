from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.inicio,
        name="inicio",
    ),

    path(
        "mi-album/",
        views.mi_album,
        name="mi_album",
    ),

    path(
        "mis-repetidas/",
        views.mis_repetidas,
        name="mis_repetidas",
    ),

    path(
        "mis-faltantes/",
        views.mis_faltantes,
        name="mis_faltantes",
    ),

    path(
        "canje/<str:username>/",
        views.posible_canje,
        name="posible_canje",
    ),

    path(
        "mi-perfil/",
        views.mi_perfil,
        name="mi_perfil",
    ),

    path(
        "u/<str:username>/",
        views.perfil_usuario,
        name="perfil_usuario",
    ),

    path(
        "mi-qr/",
        views.mi_qr,
        name="mi_qr",
    ),
    
    path(
        "posibles-canjes/",
        views.posibles_canjes,
        name="posibles_canjes",
    ),


    path(
    "mi-qr-offline/",
    views.mi_qr_offline,
    name="mi_qr_offline",
    ),

    path(
    "canje-offline/",
    views.canje_offline,
    name="canje_offline",
    ),

    path(
    "registro/",
    views.registro,
    name="registro",
    ),

    path(
    "bienvenido/",
    views.bienvenido,
    name="bienvenido",
    ),

    path(
    "descargar-album/",
    views.descargar_album_excel,
    name="descargar_album_excel",
    ),

    path(
    "cargar-album/",
    views.importar_excel,
    name="importar_excel",
    ),

    path(
    "service-worker.js",
    views.service_worker,
    name="service_worker",
    ),

    path(
    "actualizar-figurita/",
    views.actualizar_figurita_album,
    name="actualizar_figurita_album",
    ),

    path(
    "api/mi-album/",
    views.api_mi_album,
    name="api_mi_album",
    ),

    path(
    "sync-offline/",
    views.sync_offline,
    name="sync_offline",
    ),

]
