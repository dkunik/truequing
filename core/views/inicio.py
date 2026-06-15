from django.shortcuts import render
from django.db.models import Count

from core.models import AlbumUsuario, Coleccion, Figurita


def inicio(request):

    coleccion = Coleccion.objects.get(
        nombre="Mundial 2026"
    )

    figuritas = (
        Figurita.objects
        .filter(coleccion=coleccion)
        .select_related("pais")
        .order_by("pais__nombre", "numero")
    )

    paises = {}

    for figurita in figuritas:
        paises.setdefault(
            figurita.pais,
            []
        ).append(figurita)

    if request.method == "POST":

        figurita_ids = request.POST.getlist(
            "figuritas"
        )

        request.session["faltantes_iniciales"] = figurita_ids
        request.session.modified = True
        print(
            "FALTANTES GUARDADOS EN SESSION:",
            request.session.get("faltantes_iniciales")
            )

        resultados = (
            AlbumUsuario.objects
            .filter(
                figurita_id__in=figurita_ids,
                cantidad__gt=1,
            )
            .values(
                "figurita_id",
                "figurita__pais__nombre",
                "figurita__numero",
            )
            .annotate(
                usuarios=Count(
                    "usuario",
                    distinct=True,
                )
            )
            .order_by(
                "figurita__pais__nombre",
                "figurita__numero",
            )
        )

        return render(
            request,
            "core/disponibilidad.html",
            {
                "resultados": resultados,
            }
        )

    return render(
        request,
        "core/inicio.html",
        {
            "coleccion": coleccion,
            "paises": paises,
        }
    )

