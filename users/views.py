import json
import os

from django.core.management import call_command
from django.db import models
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render

from users.models import Employee


def index(request):
    return render(request, 'users/index.html')


def add_field_to_model(model_name, field_name, field_type, max_length):
    # Define the path to your models.py
    print("here we go")
    field_string = ""
    path_to_models = os.path.join(os.getcwd(), 'users', 'models.py')

    # Define the field string to append
    if field_type == "IntegerField":
        print("test two")

        field_string = f"\n    {field_name} = models.{field_type}(null=True, blank=True)\n"

    elif field_type == "CharField":
        field_string = f"\n    {field_name} = models.{field_type}(max_length={max_length}, null=True, blank=True)\n"

    # Check if field already exists
    print("test three ", field_string)
    with open(path_to_models, 'r') as file:
        if field_string in file.read():
            return f"{field_name} already exists in {model_name}"

    # Append the new field
    with open(path_to_models, 'a') as file:
        file.write(field_string)

    return f"Added {field_name} to {model_name}"




def get_field(request):
    model_name = 'Employee'
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        data = json.loads(body_unicode)

        names = data.get("names", [])
        maxChars = data.get("maxChars", [])
        dataTypes = data.get("dataTypes", [])

        for name, maxChar, dataType in zip(names, maxChars, dataTypes):
            if maxChars == ['']:
                print("none")
                add_field_to_model(model_name, field_name=name, field_type=dataType, max_length=0)
            else:
                add_field_to_model(model_name, field_name=name, field_type=dataType, max_length=maxChar)
            print(name, maxChar, dataType)
            call_command('makemigrations', 'users', no_input=True)
            call_command('migrate', 'users', no_input=True)

        return JsonResponse({'status': 'success'})

    return HttpResponseBadRequest("Invalid request method.")
