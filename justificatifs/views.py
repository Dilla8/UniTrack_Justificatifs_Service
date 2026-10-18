from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Justificatif
from .serializer import JustificatifSerializer

class JustificatifViewSet(viewsets.ModelViewSet):
    queryset = Justificatif.objects.all()
    serializer_class = JustificatifSerializer

    def get_queryset(self):
        """
        Override get_queryset to support dynamic filtering based on query parameters:
        - sender_id: filter by the user who sent the justificatif
        - target_user_id (or target_id): filter by the target recipient
        - session_id: filter by session
        """
        queryset = Justificatif.objects.all()
        sender_id = self.request.query_params.get('sender_id')
        target_user_id = self.request.query_params.get('target_user_id') or self.request.query_params.get('target_id')
        session_id = self.request.query_params.get('session_id')

        if sender_id:
            queryset = queryset.filter(sender_id=sender_id)
        if target_user_id:
            queryset = queryset.filter(target_user_id=target_user_id)
        if session_id:
            queryset = queryset.filter(session_id=session_id)

        return queryset

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        """
        Custom action to update the status and admin comment of a justificatif.
        Enforces security check to ensure only the designated target user can perform the update.
        """
        justificatif = self.get_object()
        
        # Get the requester ID from request data
        requester_id = request.data.get('requester_id')
        
        # Security validation: ensure the requester matches the target user ID
        if requester_id is not None and int(requester_id) != justificatif.target_user_id:
            return Response(
                {"error": "Unauthorized! Only the designated target user can update this justificatif status."},
                status=status.HTTP_403_FORBIDDEN
            )
            
        new_status = request.data.get('status')
        admin_comment = request.data.get('admin_comment')

        # Update status if it is valid
        if new_status in ['Accepté', 'Refusé', 'En attente']:
            justificatif.status = new_status
        
        # Update admin comment if provided
        if admin_comment is not None:
            justificatif.admin_comment = admin_comment

        justificatif.save()
        serializer = self.get_serializer(justificatif)
        return Response(serializer.data, status=status.HTTP_200_OK)
    