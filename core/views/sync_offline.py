from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def sync_offline(request):
    return render(request, "core/sync_offline.html")
