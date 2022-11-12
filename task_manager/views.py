from django.views.generic import TemplateView
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView):
    template_name = 'index.html'
    extra_context = {'title': _('Task manager')}


def error_page(request):
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the pollapp index.")
