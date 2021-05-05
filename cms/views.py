from django.shortcuts import render

from .models import Page
from ecommerce.views import BaseView


class PageView(BaseView):

    def get(self, request, page_slug):
        self.template_context['page'] = Page.objects.get(slug=page_slug)
        return render(request, 'page.html', self.template_context)






