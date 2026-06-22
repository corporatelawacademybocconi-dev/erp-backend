# Create your views here.
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Company, Tag, Contact, Interaction
from .serializers import CompanySerializer, TagSerializer, ContactSerializer, InteractionSerializer
from rest_framework.pagination import PageNumberPagination


class CompanyViewSet(viewsets.ModelViewSet):
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'industry']
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Tag.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ContactPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        from rest_framework.response import Response
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = ContactPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['company', 'relationship_score']
    search_fields = ['first_name', 'last_name', 'email', 'role', 'notes']
    ordering_fields = ['last_name', 'relationship_score', 'last_contacted']

    def get_queryset(self):
        qs = Contact.objects.filter(owner=self.request.user).select_related('company')
        role = self.request.query_params.get('role')
        if role:
            qs = qs.filter(role__icontains=role)
        return qs

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class InteractionViewSet(viewsets.ModelViewSet):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['contact', 'type']
    ordering_fields = ['date', 'created_at']

    def get_queryset(self):
        return Interaction.objects.filter(contact__owner=self.request.user)