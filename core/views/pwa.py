from django.conf import settings
from django.http import FileResponse


def service_worker(request):
    path = (
        settings.BASE_DIR
        / "core"
        / "static"
        / "core"
        / "pwa"
        / "service-worker.js"
    )

    response = FileResponse(
        open(path, "rb"),
        content_type="application/javascript",
    )

    response["Service-Worker-Allowed"] = "/"

    return response
