import django_tables2 as tables
from django_tables2.utils import A

from .models import Project


class ProjectTable(tables.Table):

    upload_prereport = tables.LinkColumn('prereport', args=[A('pk')], verbose_name= 'Prereport')
    upload_report = tables.LinkColumn('report', args=[A('pk')])
    upload_offer = tables.LinkColumn('offer', args=[A('pk')])
    upload_file = tables.LinkColumn('offer', args=[A('pk')])
    upload_permit = tables.LinkColumn('construction_permit', args=[A('pk')])
    is_date_set = tables.LinkColumn('installation_date', args=[A('pk')])

    class Meta:
        model = Project
        fields = [
            'client',
            'status',
            'warning',
            'date_prereport',
            'is_invalid_prereport',
            'upload_prereport',
            'date_report',
            'is_invalid_report',
            'upload_report',
            'date_offer',
            'upload_offer',
            'is_invalid_offer',
            'date_permit',
            'upload_permit',
            'date_start_installation',
            'is_date_set'
        ]
        #ttrs = {"class": "table-striped"}
       # template_name = 'django_tables2/bootstrap4.html'


#   def render_client(self, value):
#       return '{}'.format(value.name)

