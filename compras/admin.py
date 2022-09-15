from django.contrib import admin
from .models import Buy, ToDo


class buyAdmin(admin.ModelAdmin):
    list_display = ('toBuy', 'dateStart', 'status', 'dateEnd')

admin.site.register(Buy, buyAdmin)


class toDoAdmin(admin.ModelAdmin):
    list_display = ('toDo', 'dateStart', 'dateEnd')

admin.site.register(ToDo, toDoAdmin)
