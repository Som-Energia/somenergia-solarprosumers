from rest_framework import serializers

from somsolet.models import Project


class PrereportFileSerializer(serializers.HyperlinkedModelSerializer):

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


class SignatureFileSerializer(serializers.HyperlinkedModelSerializer):

    signatureDate = serializers.DateField(source='signature.date')
    signed = serializers.BooleanField(source='signature.check')
    signatureUpload = serializers.FileField(source='signature.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'signatureDate',
            'signed',
            'signatureUpload',
            'status'
        )


class PermitFileSerializer(serializers.HyperlinkedModelSerializer):

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


class LegalRegistrationFileSerializer(serializers.HyperlinkedModelSerializer):

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

class LegalizationFileSerializer(serializers.HyperlinkedModelSerializer):

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
