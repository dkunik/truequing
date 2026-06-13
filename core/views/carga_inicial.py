from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from core.models import AlbumUsuario, Coleccion, Figurita


def agrupar_figuritas_por_pais(figuritas):
    paises = {}

    for figurita in figuritas:
        paises.setdefault(figurita.pais, []).append(figurita)

    return paises


@login_required
def cargar_faltantes(request):
    coleccion = Coleccion.objects.get(nombre="Mundial 2026")

    figuritas = (
        Figurita.objects
        .filter(coleccion=coleccion)
        .select_related("pais")
        .order_by("pais__nombre", "numero")
    )

    if request.method == "POST":
        faltantes_ids = request.POST.getlist("figuritas")

        AlbumUsuario.objects.filter(
            usuario=request.user,
            figurita__coleccion=coleccion,
        ).update(cantidad=1)

        AlbumUsuario.objects.filter(
            usuario=request.user,
            figurita_id__in=faltantes_ids,
        ).update(cantidad=0)

        return redirect("bienvenido")

    return render(request, "core/cargar_faltantes.html", {
        "titulo": "Cargar mis faltantes",
        "descripcion": "Marcá las figuritas que todavía estás buscando.",
        "paises": agrupar_figuritas_por_pais(figuritas),
    })
@login_required
def cargar_repetidas(request):
    return redirect("mi_album")
