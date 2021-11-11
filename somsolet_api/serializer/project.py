from datetime import datetime

import pymongo
from django.conf import settings
from rest_framework import serializers
from somsolet.models import Project, Technical_details


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    stages = serializers.SerializerMethodField('get_stages')
    description = serializers.SerializerMethodField('get_project_details')

    class Meta:
        model = Project
        fields = (
            'description',
            'stages',
        )
        read_only_fields = ['description', 'stages']

    def get_engineerings(self, obj):
        return [
            {
                'name': e.name,
                'address': e.address,
                'email': e.email,
                'phoneNumber': e.phone_number,
            } for e in obj.campaign.engineerings.all()
        ]

    def get_registeredPerson(self, obj):
        return {
            'name': obj.client.name,
            'email': obj.client.email,
            'phoneNumber': obj.client.phone_number,
            'language': obj.client.language
        } if obj.client else {}

    def get_supplyPoint(self, obj):
        technical_details = Technical_details.objects.filter(
            project=obj,
        ).first()
        if technical_details:
            return {
                'cups': technical_details.cups,
                'address':
                {
                    'administrativeDivision': technical_details.administrative_division,
                    'municipality': technical_details.municipality,
                    'town': technical_details.town,
                    'street': technical_details.street,
                    'postalCode': technical_details.postal_code,
                },
                #'power': not implemented,
                'tariff': technical_details.tariff,
            }
        return {}

    def get_project_details(self, obj):
        return {
            'name': obj.name,
            'projectId': obj.id,
            'campaignName': obj.campaign.name,
            'dateStart': obj.registration_date,
            'engineerings': self.get_engineerings(obj),
            'registeredPerson': self.get_registeredPerson(obj),
            'supplyPoint': self.get_supplyPoint(obj),
            'stageId': obj.status,
            'warning': obj.warning,

        } if obj.campaign else {}

    def get_stages(self, obj):
        return {
            'registered': {
                'date': obj.registration_date
            },
            'prereport': {
                'date': obj.prereport.date,
                'invalid': obj.prereport.check,
                'file': obj.prereport.upload,
            },
            'technicalVisits': [{
                'date': date.start_date,
                'action': 'link_to_somrenkonto',
            } for date in obj.technical_visit_dates],
            'report': {
                'date': obj.report.date,
                'invalid': obj.report.check,
                'file': obj.report.upload,
            },
            'offer': {
                'date': obj.offer.date,
                'file': obj.offer.upload,
            },
            'offer_accepted': {
                'date': obj.offer.date,
                'accepted': obj.offer.check,
            },
            'signature': {
                'date': obj.signature.date,
                'file': obj.signature.upload,
            },
            'constructionPermit': {
                'date': obj.permit.date,
                'file': obj.permit.upload,
            },
            'installation': {
                'date': obj.date_start_installation,
                'dateSet': obj.is_date_set,
                'action': 'link_to_somrenkonto',
                'inProgress': obj.is_installation_in_progress
            },
            'deliveryCertificate': {
                'date': obj.delivery_certificate.date,
                'file': obj.delivery_certificate.upload,
            },
            'legalRegistration': {
                'date': obj.legal_registration.date,
                'file': obj.legal_registration.upload,
            },
            'legalization': {
                'date': obj.legalization.date,
                'racFile': obj.legalization.rac_file,
                'ritsicFile': obj.legalization.ritsic_file,
                'cieFile': obj.legalization.cie_file,
            },
            'invoices': {
                'first': {
                    'date': obj.first_invoice.date,
                    'file': obj.first_invoice.upload,
                },
                'second': {
                    'date': obj.second_invoice.date,
                    'file': obj.second_invoice.upload,
                },
                'last': {
                    'date': obj.date_last_invoice,
                    'file': obj.upload_last_invoice,
                }
            }
            # To Do:
            # 'discardedType'  not implemented
        }


class LastInvoiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'date_last_invoice',
            'is_paid_last_invoice',
            'upload_last_invoice',
            'status'
        )


class DownloadCchSerializer(serializers.HyperlinkedModelSerializer):
    cch_data = serializers.SerializerMethodField('get_cch')

    class Meta:
        model = Project
        fields = (
            'name',
            'is_cch_downloaded',
            'date_cch_download',
            'cch_data'
        )

    def get_cch(self, instance):
        technical_details = instance.technical_details_set.first()

        client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/{}'.format(
            settings.DATABASES['mongodb']['USER'],
            settings.DATABASES['mongodb']['PASSWORD'],
            settings.DATABASES['mongodb']['HOST'],
            settings.DATABASES['mongodb']['PORT'],
            settings.DATABASES['mongodb']['NAME'],
        )
        )
        db = client[settings.DATABASES['mongodb']['NAME']]

        cursor = db.tg_cchfact.find({
            "name": {'$regex': '^{}'.format(technical_details.cups[:20])}
        })
        if cursor.count() == 0:
            return {}
        else:
            cch_data = [
                {
                    'project': instance.name,
                    'date': measure['datetime'],
                    'value': measure['ai'],
                    'units': 'Wh'
                } for measure in cursor]
            client.close()
            instance.is_cch_downloaded = True
            instance.date_cch_download = datetime.now().strftime('%Y-%m-%d')
            instance.save()
            return cch_data


class TechnicalDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Technical_details
        exclude = ['client']
