from django.shortcuts import render
from django.views.generic.edit import FormView, ModelFormMixin, CreateView
from django.views.generic.base import TemplateView
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import SignUpForm, LoginForm, ProfileForm, CareerForm
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
    success_url = 'profile/add-career'
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
            pass
        else:
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
            print('in profile except')
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
        print(user)
        try:
            careers = StudentCareer.objects.filter(user=student)
        except:
            careers = []
        finally:
            context['careers'] = careers
            print(careers)
            return context

from django.forms import formset_factory
from django.views.generic.base import View

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

class CareerView(LoginRequiredMixin, FormView):
    template_name = 'add-career.html'
    form_class = CareerForm
    success_url = '/profile'

    def form_valid(self, form):
        user = self.request.user
        student = CustomUser.objects.get(username=str(user))
        career = form.save(commit=False)
        career.user = student
        career.save()
        return super().form_valid(form)


    # def get(self, request, *args, **kwargs):
    #     return render(
    #         request,
    #         template_name='add-career.html',
    #         context={'formset': CareerFormSet})
    #
    # def post(self, request,):

