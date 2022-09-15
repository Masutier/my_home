from django.urls import path, include
from .views import *

urlpatterns = [
    path('', homePage, name="homePage"),
    path('createBuy', createBuy, name="createBuy"),
    path('updateBuy/<int:pk>/', updateBuy, name="updateBuy"),
    path('deleteBuy/<int:pk>/', deleteBuy, name="deleteBuy"),

    path('createToDo', createToDo, name="createToDo"),
    path('updateToDo/<int:pk>/', updateToDo, name="updateToDo"),
    path('deleteToDo/<int:pk>/', deleteToDo, name="deleteToDo"),

    path('historyBuy', historyBuy, name="historyBuy"),
    path('historyReactivate/<int:pk>/', historyReactivate, name="historyReactivate"),

    path('closeBuy', closeBuy, name="closeBuy"),
]
