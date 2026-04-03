from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import FinancialRecord
from .serializers import FinancialRecordSerializer
from .pagination import RecordPagination
from apps.roles.permissions import IsAdminUser, IsViewerOrAbove


class FinancialRecordViewSet(viewsets.ModelViewSet):
    queryset = FinancialRecord.objects.all()
    serializer_class = FinancialRecordSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['type', 'category', 'date']
    search_fields = ['notes', 'category']
    ordering_fields = ['amount', 'date']
    pagination_class = RecordPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Only admin can create / edit / delete records
            return [IsAdminUser()]
        # viewer, analyst, admin can all read records
        return [IsViewerOrAbove()]

    def get_queryset(self):
        """
        Admins see all records.
        Viewers and analysts only see their own records.
        """
        user = self.request.user
        if user.role == 'admin':
            return FinancialRecord.objects.all()
        return FinancialRecord.objects.filter(user=user)

    def perform_create(self, serializer):
        """Auto-assign the logged-in user when admin creates a record."""
        serializer.save(user=self.request.user)