from django.conf.urls import url, include
from django.contrib import admin

from django.views.generic.base import TemplateView

from dashboards.views import search_by_major, search_by_company, search_by_name, graduation_rate, studend_per_industry_rate, student_rate_by_major, salary_rate_by_major

urlpatterns = [
    # Examples:
    # url(r'^$', 'school_demo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'', include('users.urls')),
    url(r'^major-search', search_by_major, name='major-search'),
    url(r'^company-search', search_by_company, name='company-search'),
    url(r'^name-search', search_by_name, name='name-search'),
    url(r'^graduation-rate/', graduation_rate, name='graduation-rate'),
    url(r'^industry-rate/', studend_per_industry_rate, name='industry-rate'),
    url(r'^major-rate/', student_rate_by_major, name='major-rate'),
    url(r'^salary-rate/', salary_rate_by_major, name='salary-rate'),
    url(r'^faq', TemplateView.as_view(template_name='faq.html'), name='faq')
]
