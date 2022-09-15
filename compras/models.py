from django.db import models


class Buy(models.Model):
    toBuy = models.CharField(max_length=150, blank=False, null=False)
    dateStart = models.DateField(auto_now_add=True, auto_now=False)
    status = models.BooleanField(default=False)
    dateEnd = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.toBuy


class ToDo(models.Model):
    toDo = models.CharField(max_length=150, blank=False, null=False)
    dateStart = models.DateField(auto_now_add=True, auto_now=False)
    dateEnd = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)

    def __str__(self):
        return self.toDo
    