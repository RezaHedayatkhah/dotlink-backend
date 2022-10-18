import uuid
from rest_framework import serializers

from shortener.models import Link

class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['id', 'title', 'description', 'url_code', 'long_url', 'view']
        read_only_fields = ['id', 'url_code', 'view']
        
    def create(self, validated_data):
        link = Link.objects.create(
            user =  self.context['request'].user,
            title = validated_data['title'],
            description = validated_data['description'],
            url_code = str(uuid.uuid4())[:8],
            long_url = validated_data['long_url'],
        )
        return link


class PublicLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['long_url']