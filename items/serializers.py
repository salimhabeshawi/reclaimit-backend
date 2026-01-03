from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import ContactRequest, ItemPost


class ItemPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPost
        fields = (
            "id",
            "university",
            "title",
            "description",
            "location_text",
            "date_of_event",
            "is_resolved",
            "created_at",
        )
        read_only_fields = ("created_at", "is_resolved")


class ContactRequestSerializer(serializers.ModelSerializer):
    from_user_data = serializers.SerializerMethodField()
    to_user_data = serializers.SerializerMethodField()
    item_title = serializers.CharField(source="item.title", read_only=True)

    class Meta:
        model = ContactRequest
        fields = (
            "id",
            "from_user_data",
            "to_user_data",
            "item",
            "item_title",
            "is_accepted",
            "created_at",
        )
        read_only_fields = ("from_user", "to_user", "created_at", "is_accepted")

    def get_from_user_data(self, obj):
        user = self.context["request"].user
        # Finder (to_user) can always see the Claimant's (from_user) username
        if user == obj.to_user or user.is_staff:
            return UserSerializer(obj.from_user).data
        # Others see only non-sensitive info if needed, or masked
        return {"id": obj.from_user.id, "full_name": obj.from_user.full_name}

    def get_to_user_data(self, obj):
        user = self.context["request"].user
        # Claimant (from_user) sees Finder's (to_user) username ONLY IF accepted
        if (user == obj.from_user and obj.is_accepted) or user.is_staff:
            return UserSerializer(obj.to_user).data
        # Otherwise, mask the username
        return {"id": obj.to_user.id, "full_name": obj.to_user.full_name}
