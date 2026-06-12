from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook

from core.models import AlbumUsuario, Coleccion, Pais


@login_required
def descargar_album_excel(request):
    coleccion = Coleccion.objects.get(nombre="Mundial 2026")

    wb = Workbook()
    wb.remove(wb.active)

    paises = Pais.objects.filter(
        coleccion=coleccion,
    ).order_by("nombre")

    for pais in paises:
        ws = wb.create_sheet(title=pais.nombre[:31])

        ws.append(["numero", "cantidad"])

        items = (
            AlbumUsuario.objects
            .filter(
                usuario=request.user,
                figurita__pais=pais,
                figurita__coleccion=coleccion,
            )
            .select_related("figurita")
            .order_by("figurita__numero")
        )

        for item in items:
            ws.append([
                item.figurita.numero,
                item.cantidad,
            ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    response = HttpResponse(
        buffer.getvalue(),
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    response["Content-Disposition"] = 'attachment; filename="mi_album.xlsx"'

    return response
