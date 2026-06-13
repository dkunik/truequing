from django.db.models import Count, Q
from django.shortcuts import render

from core.models import AlbumUsuario, Coleccion, Figurita


def agrupar_por_pais(items):
    paises = {}

    for item in items:
        pais = item["pais"]

        if pais not in paises:
            paises[pais] = []

        paises[pais].append(item)

    return paises


def estadisticas(request):
    coleccion = Coleccion.objects.get(nombre="Mundial 2026")

    figuritas = (
        Figurita.objects
        .filter(coleccion=coleccion)
        .select_related("pais")
        .annotate(
            faltantes=Count(
                "usuarios",
                filter=Q(usuarios__cantidad=0),
                distinct=True,
            ),
            repetidas=Count(
                "usuarios",
                filter=Q(usuarios__cantidad__gt=1),
                distinct=True,
            ),
        )
        .order_by("pais__nombre", "numero")
    )

    items = []

    for figurita in figuritas:
        if figurita.repetidas == 0:
            dificultad = figurita.faltantes
        else:
            dificultad = figurita.faltantes / figurita.repetidas
        if dificultad == 0:
            clase = "dif-0"
        elif dificultad < 1:
            clase = "dif-1"
        elif dificultad < 3:
            clase = "dif-2"
        elif dificultad < 10:
            clase = "dif-3"
        else:
            clase = "dif-4"

        items.append({
            "pais": figurita.pais,
            "numero": figurita.numero,
            "faltantes": figurita.faltantes,
            "repetidas": figurita.repetidas,
            "dificultad": dificultad,
            "clase": clase,
        })

    return render(request, "core/estadisticas.html", {
        "paises": agrupar_por_pais(items),
    })
