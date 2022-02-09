from rest_framework.permissions import DjangoModelPermissions


class SomsoletAPIModelPermissions(DjangoModelPermissions):

    def __init__(self, **kwargs):
        # super().__init__(**kwargs)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']
        self.perms_map['PATCH'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['PUT'] = ['%(app_label)s.change_%(model_name)s']
        self.perms_map['POST'] = ['%(app_label)s.add_%(model_name)s']

    # def has_permission(self, request, view):
    #     import pdb; pdb.set_trace()
    #     #super().has_permission(request, view)
    #     if getattr(view, '_ignore_model_permissions', False):
    #         return True

    #     if not request.user or (
    #        not request.user.is_authenticated and self.authenticated_users_only):
    #         return False

    #     queryset = self._queryset(view)
    #     perms = self.get_required_permissions(request.method, queryset.model)

    #     does_he = request.user.has_perms(perms)

    #     return does_he