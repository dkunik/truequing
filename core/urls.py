from django.urls import path

from . import views

urlpatterns = [
        
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

    path(
    "",
    views.inicio,
    name="inicio",
    ),

    path(
    "cargar-faltantes/",
    views.cargar_faltantes,
    name="cargar_faltantes",
    ),

    path(
    "cargar-repetidas/",
    views.cargar_repetidas,
    name="cargar_repetidas",
    ),

    path(
    "estadisticas/",
    views.estadisticas,
    name="estadisticas",
    ),
    path(
    "mensaje/<str:username>/",
    views.enviar_mensaje,
    name="enviar_mensaje",
    ),

    path(
    "conversacion/<int:conversacion_id>/",
    views.ver_conversacion,
    name="ver_conversacion",
    ),

    path(
    "mensajes/",
    views.mis_conversaciones,
    name="mis_conversaciones",
    ),
]
