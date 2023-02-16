from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views import View


# Create your views here.
def index_view(request):
    return render(request, "authentification/index.html", {})


def accessibility_view(request):
    return render(request, "authentification/accessibility.html", {})


class Authorize(View):
    REQUIRED_REQUEST_PARAMETERS = (
        "scope",
        "response_type",
        "client_id",
        "redirect_uri",
    )

    def get(self, request):
        if not self.check_required_parameters(request.GET):
            return HttpResponseBadRequest()
        return HttpResponse("result")

    def post(self, request):
        if not self.check_required_parameters(request.GET):
            return HttpResponseBadRequest()
        return HttpResponse("result")

    def check_required_parameters(self, parameters):
        return all(p in parameters for p in self.REQUIRED_REQUEST_PARAMETERS)
