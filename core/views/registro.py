from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render
from django.contrib.auth import login

from core.models import AlbumUsuario, Coleccion
from core.services import inicializar_album_usuario


def registro(request):

    error = None

    if request.method == "POST":

        username = request.POST["username"].strip()
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            error = "Las contraseñas no coinciden."

        else:

            User = get_user_model()

            if User.objects.filter(
                username=username
            ).exists():

                error = "Ese usuario ya existe."

            else:

                user = User.objects.create_user(
                    username=username,
                    password=password1,
                )

                coleccion = Coleccion.objects.get(
                    nombre="Mundial 2026"
                )

                inicializar_album_usuario(
                    user,
                    coleccion,
                )

                print(
                    "SESSION EN REGISTRO:",
                    request.session.get(
                    "faltantes_iniciales"
                )
                )

                faltantes_iniciales = request.session.pop(
                        "faltantes_iniciales",
                        []
                    )
                print(

                    "FALTANTES RECUPERADOS:",

                    faltantes_iniciales

                )

                if faltantes_iniciales:
                    AlbumUsuario.objects.filter(usuario=user,).update(
                    cantidad=1

                    ) 

                    AlbumUsuario.objects.filter(
                        usuario=user,
                        figurita_id__in=faltantes_iniciales,
                    ).update(
                        cantidad=0
                    )

                login(request, user)

                return redirect("bienvenido")

    return render(
        request,
        "registration/registro.html",
        {
            "error": error,
        },
    )




