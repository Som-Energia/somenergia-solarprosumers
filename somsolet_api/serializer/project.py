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
        }

    def get_supplyPoint(self, obj):
        technical_details = Technical_details.objects.get(
            project__name=obj.name,
        )
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

        }

    def get_stages(self, obj):
        return {
            'registered': {
                'date': obj.registration_date
            },
            'prereport': {
                'date': obj.date_prereport,
                'invalid': obj.is_invalid_prereport,
                'file': obj.upload_prereport.url
            },
            'technicalVisit': {
                'date': obj.date_technical_visit,
                'action': 'link_to_somrenkonto',
            },
            'report': {
                'date': obj.date_report,
                'invalid': obj.is_invalid_report,
                'file': obj.upload_report.url
            },
            'offer': {
                'date': obj.date_offer,
                'invalid': obj.is_invalid_offer,
                'accepted': obj.is_offer_accepted,
                'file': obj.upload_offer.url
            },
            'signature': {
                'date': obj.date_signature,
                'signed': obj.is_signed,
                'file': obj.upload_contract.url,
                'action': 'link_to_signaturit'
            },
            'constructionPermit': {
                'date': obj.date_permit,
                'file': obj.upload_permit.url
            },
            'installation': {
                'date': obj.date_start_installation,
                'dateSet': obj.is_date_set,
                'action': 'link_to_somrenkonto',
                'inProgress': obj.is_installation_in_progress
            },
            'deliveryCertificate': {
                'date': obj.date_delivery_certificate,
                'file': obj.upload_delivery_certificate.url,
                'action': 'link_to_signaturit'

            },
            'legalRegistration': {
                'date': obj.date_legal_registration_docs,
                'file': obj.upload_legal_registration_docs.url
            },
            'legalization': {
                'date': obj.date_legal_docs,
                'file': obj.upload_legal_docs.url

            },
            # To Do:
            # 'invoice'  not implemented
            # 'discardedType'  not implemented
        } 
