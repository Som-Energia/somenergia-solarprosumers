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

class OfferReviewFileSerializer(serializers.HyperlinkedModelSerializer):

    offerReviewDate = serializers.DateField(source='offer_review.date')
    offerReviewUpload = serializers.FileField(source='offer_review.upload')

    class Meta:
        model = Project
        fields = (
            'id',
            'offerReviewDate',
            'offerReviewUpload',
            'status'
        )
