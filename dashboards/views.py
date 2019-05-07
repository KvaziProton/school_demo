from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView

from .forms import SearchByMajorForm, SearchByInputForm
from users.models import StudentCareer, StudentProfile, Major, Company, CustomUser


def search_by_major(request):
    context = {}

    if request.method == 'POST':
        form = SearchByMajorForm(request.POST)
        if form.is_valid():
            major = form.cleaned_data['major']
            major = Major.objects.get(pk=major)
            m1 = StudentProfile.objects.filter(major1=major)
            m2 = StudentProfile.objects.filter(major2=major)

            careers = []
            for i in m1:
                careers.append(StudentCareer.objects.filter(user=i.user))

            for i in m2:
                careers.append(StudentCareer.objects.filter(user=i.user))

            context['queryset'] = careers
    else:
        form = SearchByMajorForm()
        context['init'] = True

    context['form'] = form

    return render(request, 'search.html', context)

def search_by_company(request):
    context = {}

    if request.method == 'POST':
        form = SearchByInputForm(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data['input']
            companies = Company.objects.filter(company_name=company_name)

            queryset = []
            for company in companies:
                queryset.append(StudentCareer.objects.filter(company=company.pk))

            context['queryset'] = queryset
    else:
        form = SearchByInputForm()
        context['init'] = True

    context['form'] = form

    return render(request, 'company-search.html', context)

def search_by_name(request):
    context = {}

    if request.method == 'POST':
        form = SearchByInputForm(request.POST)
        if form.is_valid():
            names = form.cleaned_data['input'].lower()
            users = [
                (user.first_name.lower(), user.middle_name.lower(), user.last_name.lower(), str(user.pk))
                     for user in CustomUser.objects.filter(role='1')]
            result = []
            for user in users:
                if names in user:
                    result.append(user[-1])
            queryset = [
                StudentProfile.objects.get(user=int(pk)) for pk in result]

            context['queryset'] = queryset
    else:
        form = SearchByInputForm()
        context['init'] = True

    context['form'] = form

    return render(request, 'name-search.html', context)

from pylab import figure, axes, pie, title
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
from django.http import HttpResponse
import io

def test_matplotlib(request):
    f = figure(figsize=(6,6))

    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
    fracs = [15,30,45, 10]
    explode=(0, 0.05, 0, 0)
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    title('Random data', bbox={'facecolor':'0.8', 'pad':5})

    FigureCanvasAgg(f)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    return response

# sudo apt-get install python3-tk