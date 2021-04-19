from rest_framework.permissions import DjangoModelPermissions


class SomsoletAPIModelPermissions(DjangoModelPermissions):

    def __init__(self):
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['PATCH'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['PUT'] = ['%(app_label)s.view_%(model_name)s']
