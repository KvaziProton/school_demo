import io
from collections import Counter
from datetime import timedelta

import matplotlib
matplotlib.use('Agg')
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pylab import figure, axes, pie, title

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

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
            company_name = form.cleaned_data['input'].lower().capitalize()
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
            names = form.cleaned_data['input']
            users = [
                (user.first_name, user.middle_name, user.last_name, str(user.pk))
                     for user in CustomUser.objects.filter(role='1')]
            result = []

            for user in users:
                if names in user:
                    result.append(user[-1])
            queryset = []
            for pk in result:
                try:
                    queryset.append(StudentProfile.objects.get(user=int(pk)))
                except:
                    pass
            context['queryset'] = queryset
    else:
        form = SearchByInputForm()
        context['init'] = True

    context['form'] = form

    return render(request, 'name-search.html', context)

def graduation_rate(request):
    students = CustomUser.objects.filter(role='1')
    count = 0

    for student in students:
        gr_date = student.studentprofile.graduation_date
        first_emp_date = StudentCareer.objects.filter(
            user=student).order_by('employment_start_date')[0].employment_start_date
        if gr_date + timedelta(days=6 * 30) <= first_emp_date:
            count += 1

    res = count/(len(students)/100)

    f = figure(figsize=(6,6))

    ax = axes([0.1, 0.1, 0.8, 0.8])
    labels = 'Within 6 months', 'Over 6 months'
    fracs = [res, (100-res) ]
    explode=(0, 0.05)
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    title(
        'Percentage of students who got jobs within 6 months of graduation',
        bbox={'facecolor':'0.8', 'pad':5})

    # FigureCanvasAgg(f)
    buf = io.BytesIO()
    plt.savefig(buf, format='pdf')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    return response

def studend_per_industry_rate(request):
    students = CustomUser.objects.filter(role='1')

    industry_list = []
    for student in students:
        industry = StudentCareer.objects.filter(
            user=student).order_by(
            'employment_start_date')[0].company.industry_type

        industry_list.append(industry)

    labels = []
    fracs = []

    working_students = len(industry_list)
    industries = set(industry_list)
    counter = Counter(industry_list)

    for industry in industries:
        percent = counter[industry]/(working_students/100)
        fracs.append(percent)
        labels.append(industry)

    f = figure(figsize=(6, 6))

    ax = axes([0.1, 0.1, 0.8, 0.8])
    explode = [0 for i in range(len(industries))]
    explode[1] = 0.05
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    title('Percentage of students employed in each industry', bbox={'facecolor': '0.8', 'pad': 5})

    # FigureCanvasAgg(f)
    buf = io.BytesIO()
    plt.savefig(buf, format='pdf')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    return response

def salary_rate_by_major(request):
    majors = Major.objects.all()
    res = {}
    salary_range = {
        '1':'50,000 to 60,000',
        '2':'60,000 to 70,000',
        '3':'70,000 to 80,000',
        '4':'80,000 to 90,000',
        '5':'90,000 to 100,000'
    }
    with PdfPages('/static/files/salary_rate_by_major.pdf') as pdf:
        for major in majors:
            profiles = StudentProfile.objects.filter(major1=major)
            if profiles:
                res[major] = []
                for profile in profiles:
                    current_salary_range = StudentCareer.objects.filter(
                        user=profile.user).order_by(
                        'employment_start_date')[0].salary_range

                    res[major].append(current_salary_range)

                labels = []
                fracs = []
                counter = Counter(res[major])

                for salary in set(res[major]):
                    percent = counter[salary] / (len(res[major]) / 100)
                    fracs.append(percent)
                    labels.append(salary_range[salary])

                figure(figsize=(6, 6))

                ax = axes([0.1, 0.1, 0.8, 0.8])
                explode = [0 for _ in range(len(labels))]
                try:
                    explode[1] = 0.05
                except IndexError:
                    pass
                pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%',
                    shadow=True, radius=0.8)
                title('Salary rate by major: '+major.major_name,
                      bbox={'facecolor': '0.8', 'pad': 5})
                plt.gcf().subplots_adjust(bottom=0.15)
                pdf.savefig()  # saves the current figure into a pdf page
                plt.close()

        # We can also set the file's metadata via the PdfPages object:
        d = pdf.infodict()
        d['Title'] = 'Salary range by major'

    return HttpResponseRedirect('/static/files/salary_rate_by_major.pdf')

def student_rate_by_major(request):
    students = CustomUser.objects.filter(role='1')

    majors = []
    for student in students:
        major1 = StudentProfile.objects.get(user=student).major1
        major2 = StudentProfile.objects.get(user=student).major2

        majors.append(major1)
        if major2:
            majors.append(major2)

    counter = Counter(majors)

    labels = []
    fracs = []

    for major in set(majors):
        percent = counter[major] / (len(majors) / 100)
        fracs.append(percent)
        labels.append(major)

    f = figure(figsize=(6, 6))

    ax = axes([0.1, 0.1, 0.8, 0.8])
    explode = [0 for _ in range(len(labels))]
    explode[1] = 0.05
    pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, radius=0.8)
    title('Student per industry rate', bbox={'facecolor': '0.8', 'pad': 5})

    # FigureCanvasAgg(f)
    buf = io.BytesIO()
    plt.savefig(buf, format='pdf')
    plt.close(f)
    response = HttpResponse(buf.getvalue(), content_type='application/pdf')
    return response
