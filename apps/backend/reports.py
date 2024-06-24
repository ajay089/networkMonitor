from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.frontend.models import(
    Logs
)
from .serializers import (
    LogsSerializer, PaginatedLogsSerializer,
) 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100

class LogsAPIView(ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination
    
    ''' List System Configurations with Pagination '''
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name='page',
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description='Page number for pagination',
                required=False
            ),
        ],
        responses={200: 'OK', 401: 'Unauthorized'}
    )
    def list(self, request, *args, **kwargs):
        try:
            queryset = Logs.objects.all().order_by('date')

            # Filtering by date
            date_filter = request.GET.get('date', None)
            if date_filter:
                queryset = queryset.filter(date_filter=date_filter)

            # Pagination
            paginator = Paginator(queryset, self.get_page_size(request))
            page = request.GET.get('page')
            try:
                logs = paginator.page(page)
            except PageNotAnInteger:
                logs = paginator.page(1)
            except EmptyPage:
                logs = paginator.page(paginator.num_pages)

            serializer = PaginatedLogsSerializer({
                'count': paginator.count,
                'next': logs.next_page_number() if logs.has_next() else None,
                'previous': logs.previous_page_number() if logs.has_previous() else None,
                'results': logs,
                'page_size': self.get_page_size(request),  # Pass page_size back to serializer context
            }, context={'request': request})

            return Response(serializer.data)
        except Exception as e:
            raise APIException({"error": str(e)})

    def get_page_size(self, request):
        page_size_param = request.GET.get('page_size', '100')  # Default page_size is '10'
        
        try:
            page_size = int(page_size_param)
            if page_size <= 0:
                page_size = 100  # Default to 10 if page_size is non-positive
        except ValueError:
            page_size = 100  # Default to 10 if page_size_param is not a valid integer

        return page_size


   