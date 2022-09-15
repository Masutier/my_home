from django.db import models
from django.forms import ModelForm
from django import forms
from .models import *


class CreateBuyForm(ModelForm):
    class Meta:
        model = Buy
        fields = '__all__'


class CreateToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = '__all__'
