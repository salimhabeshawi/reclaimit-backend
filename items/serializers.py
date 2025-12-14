from rest_framework import serializers
from .models import ItemPost, ContactRequest
from accounts.serializers import UserSerializer

class ItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPost
        fields = ('id', 'university', 'title', 'description', 'location_text', 'date_of_event', 'is_resolved', 'created_at')
        read_only_fields = ('created_at', 'is_resolved')

class ContactRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    item_title = serializers.CharField(source='item.title', read_only=True)
    
    class Meta:
        model = ContactRequest
        fields = ('id', 'from_user', 'to_user', 'item', 'item_title', 'created_at')
        read_only_fields = ('from_user', 'to_user', 'created_at')
