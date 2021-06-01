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

