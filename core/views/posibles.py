from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.models import AlbumUsuario


def contar_coincidencias(usuario_a, usuario_b):
    faltantes_a = AlbumUsuario.objects.filter(
        usuario=usuario_a,
        cantidad=0,
    ).values_list("figurita_id", flat=True)

    repetidas_a = AlbumUsuario.objects.filter(
        usuario=usuario_a,
        cantidad__gt=1,
    ).values_list("figurita_id", flat=True)

    faltantes_b = AlbumUsuario.objects.filter(
        usuario=usuario_b,
        cantidad=0,
    ).values_list("figurita_id", flat=True)

    repetidas_b = AlbumUsuario.objects.filter(
        usuario=usuario_b,
        cantidad__gt=1,
    ).values_list("figurita_id", flat=True)

    b_tiene_para_a = AlbumUsuario.objects.filter(
        usuario=usuario_b,
        cantidad__gt=1,
        figurita_id__in=faltantes_a,
    ).count()

    a_tiene_para_b = AlbumUsuario.objects.filter(
        usuario=usuario_a,
        cantidad__gt=1,
        figurita_id__in=faltantes_b,
    ).count()

    return b_tiene_para_a, a_tiene_para_b


@login_required
def posibles_canjes(request):
    User = get_user_model()

    otros_usuarios = User.objects.exclude(id=request.user.id)

    resultados = []

    for otro in otros_usuarios:
        el_tiene_para_mi, yo_tengo_para_el = contar_coincidencias(
            request.user,
            otro,
        )

        total = el_tiene_para_mi + yo_tengo_para_el

        if total > 0:
            resultados.append({
                "usuario": otro,
                "el_tiene_para_mi": el_tiene_para_mi,
                "yo_tengo_para_el": yo_tengo_para_el,
                "total": total,
            })

    resultados.sort(
        key=lambda item: item["total"],
        reverse=True,
    )

    return render(request, "core/posibles_canjes.html", {
        "resultados": resultados,
    })
