from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from apps.backend.models import(
    SystemConfiguration, SystemIPPool,
    Department
)
from .serializers import (
    SystemConfigurationSerializer, PaginatedSystemConfigurationSerializer,
    SystemIpPoolSerializer, PaginatedSystemIpPoolSerializer
) 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SystemConfigurationAPIView(ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination

    ''' Create System Configuration '''
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['system_name', 'system_type', 'system_ip'],
            properties={
                'system_name': openapi.Schema(type=openapi.TYPE_STRING),
                'system_type': openapi.Schema(type=openapi.TYPE_STRING),
                'system_ip': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={201: 'Created', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = SystemConfigurationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Record has been saved successfully"}, status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException({"error": str(e)})

    ''' Update System Configuration '''
    @swagger_auto_schema(
        operation_id='update_system_configuration',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['system_name', 'system_type', 'system_ip'],
            properties={
                'system_name': openapi.Schema(type=openapi.TYPE_STRING),
                'system_type': openapi.Schema(type=openapi.TYPE_STRING),
                'system_ip': openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
        responses={200: 'Updated', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    @transaction.atomic
    def update(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemConfiguration.objects.get(id=id)
            serializer = SystemConfigurationSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Record has been updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemConfiguration id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})

    ''' Get System Configuration '''
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="SystemConfiguration ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: 'OK', 404: 'Not Found'}
    )
    def retrieve(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemConfiguration.objects.get(id=id)
            serializer = SystemConfigurationSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemConfiguration id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="SystemConfiguration ID", type=openapi.TYPE_INTEGER)
        ],
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemConfiguration.objects.get(id=id)
            instance.delete()
            return Response({"message": "Record has been removed successfully"}, status=202)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemConfiguration id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})
        
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
            queryset = SystemConfiguration.objects.all().order_by('system_name')

            # Filtering by system_name
            system_name = request.GET.get('system_name', None)
            if system_name:
                queryset = queryset.filter(system_name__icontains=system_name)

            # Pagination
            paginator = Paginator(queryset, self.get_page_size(request))
            page = request.GET.get('page')
            try:
                systems = paginator.page(page)
            except PageNotAnInteger:
                systems = paginator.page(1)
            except EmptyPage:
                systems = paginator.page(paginator.num_pages)

            serializer = PaginatedSystemConfigurationSerializer({
                'count': paginator.count,
                'next': systems.next_page_number() if systems.has_next() else None,
                'previous': systems.previous_page_number() if systems.has_previous() else None,
                'results': systems,
                'system_name': system_name,  # Pass system_name back to serializer context
                'page_size': self.get_page_size(request),  # Pass page_size back to serializer context
            }, context={'request': request})

            return Response(serializer.data)
        except Exception as e:
            raise APIException({"error": str(e)})

    def get_page_size(self, request):
        page_size_param = request.GET.get('page_size', '10')  # Default page_size is '10'
        
        try:
            page_size = int(page_size_param)
            if page_size <= 0:
                page_size = 10  # Default to 10 if page_size is non-positive
        except ValueError:
            page_size = 10  # Default to 10 if page_size_param is not a valid integer

        return page_size

''' System Ip Pool Class View '''
class SystemIpPoolAPIView(ViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    pagination_class = CustomPagination

    ''' Create System Configuration '''
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['from_ip_range', 'to_ip_range', 'department'],
            properties={
                'from_ip_range': openapi.Schema(type=openapi.TYPE_STRING),
                'to_ip_range': openapi.Schema(type=openapi.TYPE_STRING),
                'department': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={201: 'Created', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        try:
            serializer = SystemIpPoolSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Record has been saved successfully"}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            raise APIException({"error": str(e)})

    ''' Update System Configuration '''
    @swagger_auto_schema(
        operation_id='update_system_configuration',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['from_ip_range', 'to_ip_range', 'department'],
            properties={
                'from_ip_range': openapi.Schema(type=openapi.TYPE_STRING),
                'to_ip_range': openapi.Schema(type=openapi.TYPE_STRING),
                'department': openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
        responses={200: 'Updated', 400: 'Bad Request', 401: 'Unauthorized'},
    )
    @transaction.atomic
    def update(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemIPPool.objects.get(id=id)
            serializer = SystemIpPoolSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Record has been updated successfully"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemIPPool id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})

    ''' Get System Configuration '''
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="SystemIPPool ID", type=openapi.TYPE_INTEGER)
        ],
        responses={200: 'OK', 404: 'Not Found'}
    )
    def retrieve(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemIPPool.objects.get(id=id)
            serializer = SystemIpPoolSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemIPPool id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="SystemIPPool ID", type=openapi.TYPE_INTEGER)
        ],
        responses={204: 'No Content', 404: 'Not Found'}
    )
    def destroy(self, request, id=None, *args, **kwargs):
        try:
            instance = SystemIPPool.objects.get(id=id)
            instance.delete()
            return Response({"message": "Record has been removed successfully"}, status=202)
        except ObjectDoesNotExist:
            return Response({"error": f"SystemIPPool id #{id} not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise APIException({"error": str(e)})
        
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
            queryset = SystemIPPool.objects.all().order_by('id')

            # Filtering by system_name
            ip_range = request.GET.get('ip_range', None)
            if ip_range:
                queryset = queryset.filter(Q(from_ip_range__icontains=ip_range) | Q(to_ip_range__icontains=ip_range))

            # Pagination
            paginator = Paginator(queryset, self.get_page_size(request))
            page = request.GET.get('page')
            try:
                systems = paginator.page(page)
            except PageNotAnInteger:
                systems = paginator.page(1)
            except EmptyPage:
                systems = paginator.page(paginator.num_pages)

            serializer = PaginatedSystemIpPoolSerializer({
                'count': paginator.count,
                'next': systems.next_page_number() if systems.has_next() else None,
                'previous': systems.previous_page_number() if systems.has_previous() else None,
                'results': systems,
                'ip_range': ip_range,  # Pass system_name back to serializer context
                'page_size': self.get_page_size(request),  # Pass page_size back to serializer context
            }, context={'request': request})

            return Response(serializer.data)
        except Exception as e:
            raise APIException({"error": str(e)})

    def get_page_size(self, request):
        page_size_param = request.GET.get('page_size', '10')  # Default page_size is '10'
        
        try:
            page_size = int(page_size_param)
            if page_size <= 0:
                page_size = 10  # Default to 10 if page_size is non-positive
        except ValueError:
            page_size = 10  # Default to 10 if page_size_param is not a valid integer

        return page_size    
   