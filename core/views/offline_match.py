from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Coleccion, Figurita
from core.services import (
    calcular_canje,
    decodificar_estado_canje_compacto,
    obtener_estado_canje_usuario,
)


def agrupar_por_pais(figuritas):
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
def canje_offline(request):
    resultado = None
    error = None

    if request.method == "POST":
        payload = request.POST.get("payload", "").strip()
        coleccion = Coleccion.objects.get(nombre="Mundial 2026")

        try:
            estado_mio = obtener_estado_canje_usuario(
                request.user,
                coleccion,
            )

            estado_otro = decodificar_estado_canje_compacto(
                payload,
                coleccion,
            )

            resultado_canje = calcular_canje(
                estado_mio,
                estado_otro,
            )

            yo_tengo_para_otro = figuritas_desde_ids(
                resultado_canje["a_tiene_para_b"]
            )

            otro_tiene_para_mi = figuritas_desde_ids(
                resultado_canje["b_tiene_para_a"]
            )

            resultado = {
                "usuario_otro": estado_otro.usuario,
                "otro_tiene_para_mi": agrupar_por_pais(
                    otro_tiene_para_mi
                ),
                "yo_tengo_para_otro": agrupar_por_pais(
                    yo_tengo_para_otro
                ),
            }

        except Exception as e:
            error = f"No se pudo leer el payload: {e}"

    return render(request, "core/canje_offline.html", {
        "resultado": resultado,
        "error": error,
    })
