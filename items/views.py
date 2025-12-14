from django.shortcuts import render
from rest_framework import viewsets, permissions, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ItemPost, ContactRequest
from .serializers import ItemPostSerializer, ContactRequestSerializer

# Create your views here.
class ItemPostViewSet(viewsets.ModelViewSet):
    serializer_class = ItemPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = ItemPost.objects.all().order_by('-created_at')
        university = self.request.query_params.get('university')
        if university:
            queryset = queryset.filter(university=university)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resolve(self, request, pk=None):
        item = self.get_object()
        if item.user != request.user:
            raise exceptions.PermissionDenied("You are not the owner of this item.")
        
        item.is_resolved = True
        item.save()
        return Response({'status': 'item marked as resolved'})

class ContactRequestViewSet(viewsets.ModelViewSet):
    serializer_class = ContactRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Finder sees requests received for their items
        # Claimant sees requests sent (history)
        return ContactRequest.objects.filter(to_user=user) | ContactRequest.objects.filter(from_user=user)

    def perform_create(self, serializer):
        item = serializer.validated_data['item']
        if item.user == self.request.user:
            raise exceptions.ValidationError("You cannot request your own item.")
            
        if ContactRequest.objects.filter(item=item, from_user=self.request.user).exists():
             raise exceptions.ValidationError("You have already requested this item.")
             
        serializer.save(from_user=self.request.user, to_user=item.user)
