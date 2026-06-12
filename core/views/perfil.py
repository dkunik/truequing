from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from core.models import AlbumUsuario
import base64
from io import BytesIO
import qrcode
from django.urls import reverse

@login_required
def mi_qr(request):
    perfil_url = request.build_absolute_uri(
        reverse("perfil_usuario", args=[request.user.username])
    )

    img = qrcode.make(perfil_url)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, "core/mi_qr.html", {
        "perfil_url": perfil_url,
        "qr_base64": qr_base64,
    })

@login_required
def mi_perfil(request):
    return redirect("perfil_usuario", username=request.user.username)


@login_required
def perfil_usuario(request, username):
    User = get_user_model()
    usuario_perfil = get_object_or_404(User, username=username)

    cantidad_repetidas = AlbumUsuario.objects.filter(
        usuario=usuario_perfil,
        cantidad__gt=1,
    ).count()

    cantidad_faltantes = AlbumUsuario.objects.filter(
        usuario=usuario_perfil,
        cantidad=0,
    ).count()

    return render(request, "core/perfil.html", {
        "usuario_perfil": usuario_perfil,
        "cantidad_repetidas": cantidad_repetidas,
        "cantidad_faltantes": cantidad_faltantes,
    })
