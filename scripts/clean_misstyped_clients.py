import csv

from django.db.models import Count
from somsolet.models import Client

path = 'scripts/files/'


def run():
    clients = Client.objects.all()
    for client in clients:
        client.name = client.name.title()
        client.dni = client.dni.upper()
        client.save()
    duplicated_names = Client.objects.values('name').annotate(
        name_count=Count('name')).filter(name_count__gt=1)
    if duplicated_names:
        filename = path + 'duplicated_client_name.csv'
        header = {key for d in duplicated_names for key in d.keys()}
        with open(filename, 'w') as saveclients:
            writer = csv.DictWriter(saveclients, header)
            writer.writeheader()
            writer.writerows(duplicated_names)
