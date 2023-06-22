import pymongo
from django.conf import settings
from django_tables2 import SingleTableView


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = "filter"

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


class MongoManager:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            connection_str = cls.build_connection_str()
            cls._client = pymongo.MongoClient(connection_str)
        return cls._client

    @staticmethod
    def build_connection_str():
        passw = settings.DATABASES["mongodb"].get("PASSWORD")
        user = settings.DATABASES["mongodb"].get("USER")

        passw_str = passw and f":{passw}" or ""
        user_str = user and f"{user}{passw_str}@" or ""
        host_str = (
            f"{settings.DATABASES['mongodb']['HOST']}:"
            f"{settings.DATABASES['mongodb']['PORT']}"
        )
        db = settings.DATABASES["mongodb"]["NAME"]

        return f"mongodb://{user_str}{host_str}/{db}"
