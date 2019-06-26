import django_filters
from .models import Project

class ProjectListFilter(django_filters.FilterSet):

	client = django_filters.CharFilter(lookup_expr='icontains')

	class Meta:
		model = Project
		fields = ['status', 'warning']
