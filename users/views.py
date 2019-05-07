from django.shortcuts import render
from django.views.generic.edit import FormView, ModelFormMixin, CreateView
from django.views.generic.base import TemplateView
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, LoginForm, ProfileForm, CareerForm, AdminProfileForm
from .models import CustomUser, StudentProfile, StudentCareer

def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = form.cleaned_data['email'].split('@')[0]
            user = CustomUser.objects.create_user(username,
                                            cd['email'],
                                            cd['password'])
            user.role = cd['role']
            if user.role == '0':  # admin user
                user.is_superuser = True

            user.save()

            user = auth.authenticate(username=username,
                                     password=cd['password'])
            auth.login(request, user)
            return HttpResponseRedirect('/dashboard')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def sign_in(request):
    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['email'].split('@')[0]
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                context['invalid'] = True
    else:
        form = LoginForm()

    context['form'] = form

    return render(request, 'registration/login.html', context)


class ProfileCreateView(LoginRequiredMixin, FormView):
    template_name = 'profile.html'
    form_class = ProfileForm
    success_url = '/profile'
    user_fields = ['first_name', 'middle_name', 'last_name', 'email']

    def get_initial(self):
        initial = {}
        user = self.request.user
        student = CustomUser.objects.get(username=str(user))
        for value in self.user_fields:
            initial[value] = getattr(student, value)
        try:
            profile = student.studentprofile
        except:
            initial['creation'] = True
        else:
            initial['creation'] = False
            for value in self.form_class().fields.keys():
                initial[value] = getattr(profile, value)
        finally:
            return initial

    def form_valid(self, form):
        user = self.request.user
        student = CustomUser.objects.get(username=str(user))
        cd = form.cleaned_data
        if form.has_changed():
            for field in form.changed_data:
                if field in self.user_fields:
                    setattr(student, field, cd[field])
            student.save()
        try:
            profile = student.studentprofile
        except:
            profile = form.save(commit=False)
            profile.user = student
            profile.save()
        else:
            if form.has_changed():
                for field in form.changed_data:
                    if field not in self.user_fields:
                        setattr(profile, field, cd[field])
                profile.save()
        finally:
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        student = CustomUser.objects.get(username=str(user))
        try:
            careers = StudentCareer.objects.filter(
                user=student).order_by('employment_start_date')
        except:
            careers = []
        finally:
            context['careers'] = careers
            return context


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'


class CareerView(LoginRequiredMixin, FormView):
    template_name = 'add-career.html'
    form_class = CareerForm
    success_url = '/profile'
    career_fields = ['job_role', 'employment_start_date', 'employment_end_date',
                     'enrollment_status', 'salary_range']

    def form_valid(self, form):
        cd = form.cleaned_data
        company = form.save()

        user = self.request.user
        student = CustomUser.objects.get(username=str(user))

        career = StudentCareer()
        for field in form.changed_data:
            if field in self.career_fields:
                setattr(career, field, cd[field])
        career.save()
        career.company = company
        career.user = student
        career.save()

        return super().form_valid(form)

class AdminProfileView(ProfileCreateView):
    template_name = 'profile.html'
    form_class = AdminProfileForm
    success_url = '/profile/admin'

    def form_valid(self, form):
        user = self.request.user
        admin = CustomUser.objects.get(username=str(user))
        cd = form.cleaned_data
        if form.has_changed():
            for field in form.changed_data:
                if field in self.user_fields:
                    setattr(admin, field, cd[field])
            admin.save()
        try:
            profile = admin.adminprofile
        except:
            profile = form.save(commit=False)
            profile.user = admin
            profile.save()
        else:
            if form.has_changed():
                for field in form.changed_data:
                    if field not in self.user_fields:
                        setattr(profile, field, cd[field])
                profile.save()
        finally:
            return super().form_valid(form)

    def get_initial(self):
        initial = {}
        user = self.request.user
        student = CustomUser.objects.get(username=str(user))
        for value in self.user_fields:
            initial[value] = getattr(student, value)
        try:
            profile = student.adminprofile
        except:
            initial['creation'] = True
        else:
            initial['creation'] = False
            for value in self.form_class().fields.keys():
                initial[value] = getattr(profile, value)
        finally:
            return initial