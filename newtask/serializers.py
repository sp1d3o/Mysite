from rest_framework import serializers
from .models import Category, Task

class Categoryserializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ['name']

class Taskserializer(serializers.Serializer):
    class Meta:
        model = Task
        fields = '__all__'