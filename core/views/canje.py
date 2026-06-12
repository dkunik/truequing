from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from core.models import Coleccion, Figurita
from core.services import calcular_canje, obtener_estado_canje_usuario


def agrupar_figuritas_por_pais(figuritas):
    paises = {}

    for figurita in figuritas:
        pais = figurita.pais

        if pais not in paises:
            paises[pais] = []

        paises[pais].append(figurita)

    return paises


def figuritas_desde_ids(ids):
    return (
        Figurita.objects
        .filter(id__in=ids)
        .select_related("pais")
        .order_by("pais__nombre", "numero")
    )


@login_required
def posible_canje(request, username):
    User = get_user_model()

    otro_usuario = get_object_or_404(User, username=username)
    coleccion = Coleccion.objects.get(nombre="Mundial 2026")

    estado_mio = obtener_estado_canje_usuario(
        request.user,
        coleccion,
    )

    estado_otro = obtener_estado_canje_usuario(
        otro_usuario,
        coleccion,
    )

    resultado = calcular_canje(
        estado_mio,
        estado_otro,
    )

    yo_tengo_para_el = figuritas_desde_ids(
        resultado["a_tiene_para_b"]
    )

    el_tiene_para_mi = figuritas_desde_ids(
        resultado["b_tiene_para_a"]
    )

    return render(request, "core/posible_canje.html", {
        "otro_usuario": otro_usuario,
        "yo_tengo_para_el": agrupar_figuritas_por_pais(yo_tengo_para_el),
        "el_tiene_para_mi": agrupar_figuritas_por_pais(el_tiene_para_mi),
    })
