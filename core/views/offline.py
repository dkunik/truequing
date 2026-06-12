import base64
from io import BytesIO
import qrcode
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from core.models import Coleccion
from core.services import exportar_estado_canje_compacto


@login_required
def mi_qr_offline(request):
    coleccion = Coleccion.objects.get(nombre="Mundial 2026")

    payload_qr = exportar_estado_canje_compacto(
        usuario=request.user,
        coleccion=coleccion,
    )

    img = qrcode.make(payload_qr)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")
    print(
    "Payload QR:",
    len(payload_qr),
    "bytes"
    )

    return render(request, "core/mi_qr_offline.html", {
        "qr_base64": qr_base64,
        "payload": payload_qr,
    })
