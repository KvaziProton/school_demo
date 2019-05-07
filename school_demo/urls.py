from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic.base import TemplateView

from dashboards.views import search_by_major, search_by_company, search_by_name, test_matplotlib

urlpatterns = [
    # Examples:
    # url(r'^$', 'school_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'', include('users.urls')),
    url(r'^major-search', search_by_major, name='major-search'),
    url(r'^company-search', search_by_company, name='company-search'),
    url(r'^name-search', search_by_name, name='name-search'),
    url(r'^pie/', test_matplotlib, name='test-pie'),
    url(r'^faq', TemplateView.as_view(template_name='faq.html'), name='faq')
]
