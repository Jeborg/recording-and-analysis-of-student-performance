import django_filters

from django_filters import DateFilter, CharFilter
from .models import *

class AcademicPerformanceFilter(django_filters.FilterSet):

    # description = CharFilter (field_name = '', lookup_expr = 'icontains')

    class Meta:
        model = Group
        fields = '__all__'
        exclude = ['id', 'student_id', 'subject_id']