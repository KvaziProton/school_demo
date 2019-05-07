from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import sign_up, sign_in, ProfileCreateView, DashboardView, CareerView, AdminProfileView
from dashboards.views import search_by_major, search_by_company, search_by_name 

urlpatterns = [
    url(r'^signup/', sign_up, name='signup'),
    url(r'^login/', sign_in, name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^dashboard', DashboardView.as_view(template_name='dashboard.html'), name='dashboard'),
    url(r'^profile/add-career', CareerView.as_view(), name='add-career'),
    url(r'^profile/admin', AdminProfileView.as_view(), name='admin-profile'),
    url(r'^profile', ProfileCreateView.as_view(), name='profile'),
    url(r'^major-search', search_by_major, name='major-search'),
    url(r'^company-search', search_by_company, name='company-search'),
    url(r'^name-search', search_by_name, name='name-search'),
]