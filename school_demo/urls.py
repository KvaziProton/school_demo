from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic.base import TemplateView

urlpatterns = [
    # Examples:
    # url(r'^$', 'school_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'', include('users.urls')),

    url(r'^faq', TemplateView.as_view(template_name='faq.html'), name='faq')
]
