from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import Coleccion
from core.services import importar_album_desde_excel


@login_required
def importar_excel(request):
    mensaje = None
    error = None
    errores = []

    if request.method == "POST":
        archivo = request.FILES.get("archivo")

        if not archivo:
            error = "Tenés que elegir un archivo .xlsx."
        else:
            coleccion = Coleccion.objects.get(nombre="Mundial 2026")

            resultado = importar_album_desde_excel(
                usuario=request.user,
                coleccion=coleccion,
                archivo=archivo,
            )

            mensaje = (
                f"Álbum importado correctamente. "
                f"Se actualizaron {resultado['actualizadas']} figuritas."
            )

            errores = resultado["errores"]

    return render(
        request,
        "core/importar_excel.html",
        {
            "mensaje": mensaje,
            "error": error,
            "errores": errores,
        },
    )
