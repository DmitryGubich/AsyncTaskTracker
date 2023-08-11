from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic


@method_decorator(login_required, name="dispatch")
class MainView(generic.TemplateView):
    template_name = "base.html"
