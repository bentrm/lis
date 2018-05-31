from django.views.generic import TemplateView

from cms.models import HomePage, AuthorPage, LocationPage, MemorialSitePage

class IndexView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["homepage"] = HomePage.objects.first()
        context["authors_count"] = AuthorPage.objects.count()
        context["locations_count"] = LocationPage.objects.count()
        context["memorial_sites_count"] = MemorialSitePage.objects.count()
        return context

class ImpressumView(TemplateView):
    template_name = "home/impressum.html"
