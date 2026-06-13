from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from core.models import Conversacion, Mensaje


User = get_user_model()


def obtener_conversacion(usuario_a, usuario_b):
    conversacion = (
        Conversacion.objects
        .filter(
            Q(usuario_a=usuario_a, usuario_b=usuario_b)
            |
            Q(usuario_a=usuario_b, usuario_b=usuario_a)
        )
        .first()
    )

    if conversacion is None:
        conversacion = Conversacion.objects.create(
            usuario_a=usuario_a,
            usuario_b=usuario_b,
        )

    return conversacion


@login_required
def enviar_mensaje(request, username):
    destinatario = get_object_or_404(
        User,
        username=username,
    )

    if destinatario == request.user:
        return redirect("posibles_canjes")

    conversacion = obtener_conversacion(
            request.user,
            destinatario,
        )

    if request.method == "POST":
        texto =request.POST.get("texto", "").strip()

        if texto:
            Mensaje.objects.create(
                conversacion=conversacion,
                autor=request.user,
                texto=texto,
            )

        return redirect(
            "ver_conversacion",
            conversacion_id=conversacion.id,
        )

    return render(request, "core/enviar_mensaje.html", {
        "destinatario": destinatario,
        "conversacion": conversacion,
    })


@login_required
def ver_conversacion(request, conversacion_id):
    conversacion = get_object_or_404(
        Conversacion,
        id=conversacion_id,
    )

    if request.user not in [
        conversacion.usuario_a,
        conversacion.usuario_b,
    ]:
        return redirect("posibles_canjes")

    if request.method == "POST":
        texto =request.POST.get("texto", "").strip()

        if texto:
            Mensaje.objects.create(
                conversacion=conversacion,
                autor=request.user,
                texto=texto,
            )

        return redirect(
            "ver_conversacion",
            conversacion_id=conversacion.id,
        )

    mensajes =conversacion.mensajes.all()

    return render(request, "core/conversacion.html", {
        "conversacion": conversacion,
        "mensajes": mensajes,
    })

@login_required
def mis_conversaciones(request):

    conversaciones = (
        Conversacion.objects
        .filter(
            Q(usuario_a=request.user)
            |
            Q(usuario_b=request.user)
        )
        .order_by("-fecha_creacion")
    )

    return render(
        request,
        "core/mis_conversaciones.html",
        {
            "conversaciones": conversaciones,
        }
    )
