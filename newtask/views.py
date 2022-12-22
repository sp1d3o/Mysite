from django.shortcuts import render
from .serializers import Categoryserializer, Taskserializer
from rest_framework import viewsets
from rest_framework import permissions
from .models import Category, Task
from rest_framework.response import Response
import datetime as dt

def create_new_task(request):
    new_task = Taskserializer(data=request.data)
    #created_by vyplní frontend
    #created_at je vyplněno automaticky současným časem

    if new_task.is_valid():
        new_task.save()
        return Response("Task created")
    else:
        return Response("Task not created")

def check_accessibility(data, target):

    try:
        new_data = data[target]
    except:
        None
    else:
        #should not be
        return True

    return False



def update_task(request, task_id):
    tmp = Task.objects.get(id=task_id)

    data = request.data

    if check_accessibility(data,'created_by') or check_accessibility(data, 'assigned_by') or check_accessibility(data, 'created_at') or check_accessibility(data, 'completed_at'):
        return Response("These attributes are not accessible")

    if data['assigned'] == None:
        data['assigned_at'] = None

    current_time = dt.datetime.now()

    if tmp.state == Task.ISSUE_DONE:
        data['completed_at'] = current_time
    if tmp.state == Task.ISSUE_CANCELED:
        data['completed_at'] = current_time

    return Response("Changed succesfully")

def delete_task(request, task_id):
    tmp = Task.objects.get(id=task_id)

    tmp.delete()

    try:
        control = Task.objects.get(id=task_id)
    except:
        return Response("Succesfully deleted")
    else:
        return Response("Error occured")

def retrieve_task(request, task_id):

    try:
        task = Task.objects.get(id=task_id)
    except task.DoesNotExist:
        return Response("Cannot be retrieved")
    else:
        serializer = Taskserializer(task)
        return Response(serializer.data)

def my_tasks(request):
    tmp = Task.objects.exclude(assigned=None)

    serializer = Taskserializer(tmp, many=True)

    return Response(serializer.data)

