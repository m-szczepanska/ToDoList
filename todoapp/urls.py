from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from todoapp import views

urlpatterns = [
    path('users/', views.user_list),
    path('users/<int:id>', views.user_details),
    path('items/', views.item_list),
    path('items/<int:id>', views.item_details),
    path('item_create/<int:user_id>', views.item_create),
    path('item_update/<int:id>/<int:user_id>', views.item_update),
    path('index/', views.index, name="index"),
]

urlpatterns = format_suffix_patterns(urlpatterns)