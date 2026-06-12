from django.shortcuts import redirect


def inicio(request):

    if request.user.is_authenticated:
        return redirect("mi_album")

    return redirect("/accounts/login/")
