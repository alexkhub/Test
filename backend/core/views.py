from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status

from .serializers import CreateFileSerializer, FileSerializer
from .tasks import interest_calculation
from .service import delete_old_file
from .utils import FileFilter
from rest_framework.response import Response
from .models import File
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView


class FileCreateView(CreateAPIView):
    queryset = File.objects.all()
    serializer_class = CreateFileSerializer

    def create(self, request, *args, **kwargs):
        file_serializer = self.get_serializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            interest_calculation.delay(file_serializer.data['id'])
            return Response({'message': 'Data added'}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = FileFilter


class FileRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response({'message' : 'Data update'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        delete_old_file(instance.file.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
