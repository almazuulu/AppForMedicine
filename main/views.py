import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, CreateView, TemplateView, FormView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import UserPassesTestMixin

from main.models import *
from .forms import *


def role_redirect(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    if KinderGarden.objects.filter(user=user).exists():
        return redirect('kg_dashboard')
    if Pediatrist.objects.filter(user=user).exists():
        return redirect('doctors_dashboard')
    if Parent.objects.filter(user=user).exists():
        return redirect('parents_dashboard')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('role_redirect')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


class UserIsDoctorMixin(UserPassesTestMixin):
    def test_func(self):
        return Pediatrist.objects.filter(user=self.request.user).exists()

    def handle_no_permission(self):
        if self.raise_exception:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect('role_redirect')


class Form26FormView(LoginRequiredMixin, TemplateView):
    template_name = 'main/form26_form.html'

    def get_context_data(self, *args, **kwargs):
        print(args, kwargs, self.request.GET)
        page_number = self.request.GET.get('page', 1)
        context = super(Form26FormView, self).get_context_data(*args, **kwargs)
        child_id = kwargs['child_id']

        context['child'] = Child.objects.get(pk=child_id)

        paginator = Paginator(Form26.objects.filter(child=child_id), 5)
        context['pastforms'] = paginator.get_page(page_number)

        context["is_doctor"] = Pediatrist.objects.filter(user=self.request.user.pk).exists()

        context['form'] = Form26Form

        return context

    def post(self, request, *args, **kwargs):
        child_id = kwargs['child_id']
        form_data = Form26Form(request.POST)
        if form_data.is_valid():
            Form26.objects.create(**form_data.cleaned_data, child=Child.objects.get(pk=child_id)).save()
        return redirect('form26_form', child_id)




class KinderGartenDashboardTemplateView(TemplateView):
    template_name = "main/kg_dashboard.html"

    def get(self, request, *args, **kwargs):
        print(request.user.pk)

        return super(KinderGartenDashboardTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(KinderGartenDashboardTemplateView, self).get_context_data(**kwargs)

        kg_doctors = DoctorKinderGarden.objects.filter(
            kinder_garden=KinderGarden.objects.get(
                user=self.request.user.pk).pk).values_list(
                    'pediatrist', flat=True)

        context["pediatrists"] = Pediatrist.objects.filter(pk__in=kg_doctors)
        context["surveys"] = Survey.objects.all()

        return context


class ParentsDashboardTemplateView(TemplateView):
    template_name = "main/parent_dashboard.html"

    def get(self, request, *args, **kwargs):
        print(request.user.pk)

        return super(ParentsDashboardTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ParentsDashboardTemplateView, self).get_context_data(**kwargs)
        context["pediatrists"] = Pediatrist.objects.all()
        context["surveys"] = Survey.objects.all()

        return context


class DoctorsDashboardTemplateView(TemplateView):
    template_name = "main/doctor_dashboard.html"

    def get(self, request, *args, **kwargs):
        print(request.user.pk)

        return super(DoctorsDashboardTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DoctorsDashboardTemplateView, self).get_context_data(**kwargs)

        kg_doctors = DoctorKinderGarden.objects.filter(pediatrist=self.request.user.pk).values_list('kinder_garden',
                                                                                               flat=True)
        context["kgs"] = KinderGarden.objects.filter(pk__in=kg_doctors)
        context["surveys"] = Survey.objects.all()


        return context


class DoctorsTemplateView(TemplateView):
    template_name = "main/doctors.html"

    def get_context_data(self, **kwargs):
        context = super(DoctorsTemplateView, self).get_context_data(**kwargs)
        context["pediatrists"] = Pediatrist.objects.all()

        return context


class ChildListTemplateView(TemplateView):
    template_name = "main/child_listview.html"

    def get_context_data(self, **kwargs):
        user_id = self.request.user.pk
        page_number = self.request.GET.get('page', 1)

        context = super(ChildListTemplateView, self).get_context_data(**kwargs)

        context["is_doctor"] = Pediatrist.objects.filter(user=user_id).exists()

        if Pediatrist.objects.filter(user=user_id).exists():
            kg_doctors = DoctorKinderGarden.objects.filter(
                pediatrist=user_id
            ).values_list('kinder_garden', flat=True)
            paginator = Paginator(Child.objects.filter(kinder_garden__pk__in=kg_doctors), 10)

        elif Parent.objects.filter(user=user_id).exists():
            parent = Parent.objects.get(user=user_id)
            paginator = Paginator(Child.objects.filter(Q(parent1_id=parent.pk) | Q(parent2_id=parent.pk)), 10)

        elif KinderGarden.objects.filter(user=user_id).exists():
            paginator = Paginator(Child.objects.filter(kinder_garden__pk=KinderGarden.objects.get(user=user_id).pk), 10)

        else:
            return redirect('role_redirect')

        context["children"] = paginator.get_page(page_number)

        return context
