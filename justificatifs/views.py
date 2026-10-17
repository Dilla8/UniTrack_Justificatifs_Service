from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Justificatif
from .serializer import JustificatifSerializer

class JustificatifViewSet(viewsets.ModelViewSet):
    queryset = Justificatif.objects.all()
    serializer_class = JustificatifSerializer

    @action(detail=True, methods=['patch'], url_path='update-status')
    def update_status(self, request, pk=None):
        justificatif = self.get_object()
        
        # Safe data extraction
        data = request.data
        if hasattr(data, 'get'):
            new_status = data.get('status')
            admin_comment = data.get('admin_comment', '')
        else:
            import json
            try:
                parsed_data = json.loads(data)
                new_status = parsed_data.get('status')
                admin_comment = parsed_data.get('admin_comment', '')
            except:
                new_status = None
                admin_comment = ''

        # Validation for valid status values
        valid_statuses = [choice[0] for choice in Justificatif.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return Response(
                {"error": f"Invalid status. Choose from: {valid_statuses}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update fields
        justificatif.status = new_status
        if admin_comment:
            justificatif.admin_comment = admin_comment
            
        justificatif.save()

        serializer = self.get_serializer(justificatif)
        return Response(serializer.data, status=status.HTTP_200_OK)