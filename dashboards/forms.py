from django import forms

from users.models import Major

def get_majors_list():
    query = [(i.pk, i.major_name) for i in Major.objects.all()]
    return query

class SearchByMajorForm(forms.Form):
    major = forms.ChoiceField(choices=get_majors_list)

class SearchByInputForm(forms.Form):
    input = forms.CharField()