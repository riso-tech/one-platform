from django.views.generic import TemplateView


class RenderView(TemplateView):
    template_name = "pages/home.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["css"] = open("one/static/metronic/css/style.bundle.css").read()
        context["section"] = open("one/templates/pages/_section.html").read()

        return context
