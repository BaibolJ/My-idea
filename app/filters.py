import django_filters
from .models import *
from django_filters import rest_framework as filters


class VarietyFilter(django_filters.FilterSet):
    is_this = filters.ModelChoiceFilter(queryset=Objects.objects.all())

    class Meta:
        model = Variety
        fields = ['is_this']
