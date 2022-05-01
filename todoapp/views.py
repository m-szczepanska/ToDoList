from django.shortcuts import render


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from todoapp.models import (
    User, Item
)
from todoapp.serializers import (
    GetUserSerializer, CreateUserSerializer,
    ItemSerializer)

from todoapp.services import (
    MinimumLengthValidator, NumericPasswordValidator)


@csrf_exempt
def user_list(request):
    """
    List all users.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = GetUserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CreateUserSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_user = User(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email']
        )
        new_user.set_password(data['password'])  # also saves the instance

        serializer_return = GetUserSerializer(new_user)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def user_details(request, id):
    """
    User details with a list of user items
    """
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExists:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = GetUserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        # No changing passwords here!
        data = request.json()
        data = JSONParser().parse(request)
        serializer = UpdateUserSerializer(user, data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.email = data['email']
        user.save()

        serializer_return = GetUserSerializer(user)
        return JsonResponse(serializer_return.data, safe=False)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)


@csrf_exempt
def item_list(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return JsonResponse(serializer.data, safe=False)

@csrf_exempt
def item_create(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ItemSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(serializer.errors, status=400)

        new_item = Item.objects.create(
            title=data['title'],
            text=data['text'],
            status=data['status'],
            category=data['category'],
            due_date=data['due_date'],
            user=user
        )

        serializer_return = ItemSerializer(new_item)
        return JsonResponse(serializer_return.data, safe=False, status=201)


@csrf_exempt
def item_details(request, id):
    try:
        item = Item.objects.get(id=id)
    except Item.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        item = Item.objects.get(id=id)
        serializer = ItemSerializer(item)
        return JsonResponse(serializer.data)

    elif request.method == "DELETE":
        item.delete()
        return HttpResponse(status=204)
