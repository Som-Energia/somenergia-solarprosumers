from rest_framework import serializers

from somsolet.models import Project


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