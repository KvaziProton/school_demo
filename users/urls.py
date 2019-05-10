from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import sign_up, sign_in, ProfileCreateView, DashboardView, CareerView, AdminProfileView, show_profile

urlpatterns = [
    url(r'^signup/', sign_up, name='signup'),
    url(r'^login/', sign_in, name='login'),
    url(r'^logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
    url(r'^dashboard', DashboardView.as_view(template_name='dashboard.html'), name='dashboard'),
    url(r'^profile/add-career', CareerView.as_view(), name='add-career'),
    url(r'^profile/admin', AdminProfileView.as_view(), name='admin-profile'),
    url(r'^profile/edit', ProfileCreateView.as_view(), name='profile'),
    url(r'^profile', show_profile, name='show-profile')
]