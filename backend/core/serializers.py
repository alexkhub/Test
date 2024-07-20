from rest_framework import serializers
from .models import File
from .service import delete_old_file
from .tasks import interest_calculation


class CreateFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'file')


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id', 'name', 'file', 'percentage', 'date')

    def update(self, instance, validated_data):
        if validated_data.get('file', False):
            delete_old_file(instance.file.path)
            instance.save()
            interest_calculation.delay(id=instance.id)

        return super().update(instance, validated_data)
