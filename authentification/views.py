from django.shortcuts import render


# Create your views here.
def index_view(request):
    return render(request, "authentification/index.html", {})


def accessibility_view(request):
    return render(request, "authentification/accessibility.html", {})
