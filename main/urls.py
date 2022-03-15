from django.contrib.auth.views import LoginView
from django.urls import path
from .views import *

urlpatterns = [
    path('', role_redirect, name="role_redirect"),

    path('login/', LoginView.as_view(template_name='main/login.html'), name='login'),
    path('register/', signup, name='register'),

    path('kinder_garten/home/', KinderGartenDashboardTemplateView.as_view(), name="kg_dashboard"),
    path('parent/home/', ParentsDashboardTemplateView.as_view(), name="parents_dashboard"),
    path('doctors/home/', DoctorsDashboardTemplateView.as_view(), name="doctors_dashboard"),

    path('form/child/<int:child_id>/', Form26FormView.as_view(), name="form26_form"),
    path('children/', ChildListTemplateView.as_view(), name="child_list"),

    path('doctors/', DoctorsTemplateView.as_view(), name="doctors")
]