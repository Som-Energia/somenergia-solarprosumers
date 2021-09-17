from rest_framework import serializers

from somsolet.models import Project


class PrereportStageSerializer(serializers.HyperlinkedModelSerializer):

    prereportDate = serializers.DateField(source='prereport.date')
    invalidPrereport = serializers.BooleanField(source='prereport.check')
    prereportUpload = serializers.FileField(source='prereport.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'prereportDate',
            'invalidPrereport',
            'prereportUpload',
            'status'
        )


class SignatureStageSerializer(serializers.HyperlinkedModelSerializer):

    signatureDate = serializers.DateField(source='signature.date')
    signatureUpload = serializers.FileField(source='signature.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'signatureDate',
            'signatureUpload',
            'status'
        )


class PermitStageSerializer(serializers.HyperlinkedModelSerializer):

    permitDate = serializers.DateField(source='permit.date')
    permitUpload = serializers.FileField(source='permit.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'permitDate',
            'permitUpload',
            'status'
        )


class OfferStageSerializer(serializers.HyperlinkedModelSerializer):

    offerDate = serializers.DateField(source='offer.date')
    offerUpload = serializers.FileField(source='offer.upload')
    isOfferAccepted = serializers.BooleanField(source='offer.check')

    class Meta:
        model = Project
        fields = (
            'id',
            'offerDate',
            'offerUpload',
            'isOfferAccepted',
            'status'
        )


class SecondInvoiceStageSerializer(serializers.HyperlinkedModelSerializer):

    secondInvoiceDate = serializers.DateField(source='second_invoice.date')
    secondInvoiceUpload = serializers.FileField(source='second_invoice.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'secondInvoiceDate',
            'secondInvoiceUpload',
            'status'
        )


class LegalRegistrationStageSerializer(serializers.HyperlinkedModelSerializer):

    legalRegistrationDate = serializers.DateField(source='legal_registration.date')
    legalRegistrationUpload = serializers.FileField(source='legal_registration.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'legalRegistrationDate',
            'legalRegistrationUpload',
            'status'
        )

class LegalizationStageSerializer(serializers.HyperlinkedModelSerializer):

    legalizationDate = serializers.DateField(source='legalization.date')
    legalizationRac = serializers.FileField(source='legalization.rac_file')
    legalizationRitsic = serializers.FileField(source='legalization.ritsic_file')
    legalizationCie = serializers.FileField(source='legalization.cie_file')

    class Meta:
        model = Project
        fields = (
            'id',
            'legalizationDate',
            'legalizationRac',
            'legalizationRitsic',
            'legalizationCie',
            'status'
        )

class DeliveryCertificateStageSerializer(serializers.HyperlinkedModelSerializer):

    deliveryCertificateDate = serializers.DateField(source='delivery_certificate.date')
    deliveryCertificateUpload = serializers.FileField(source='delivery_certificate.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'deliveryCertificateDate',
            'deliveryCertificateUpload',
            'status'
        )
