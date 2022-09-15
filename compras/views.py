import io
import os
import datetime
import json
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from .models import *
from .forms import *
#xls
from openpyxl import Workbook
#mail
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


# HOME
def homePage(request):
    objBuyAll = Buy.objects.all()
    objBuy = Buy.objects.filter(status='True')
    history = Buy.objects.filter(status='False')
    objToDo = ToDo.objects.all()

    context = {"title": "My Home", 'objBuy':objBuy, 'objToDo': objToDo, 'history': history}
    return render(request, "compras/homePage.html", context)


# TO DO
def createToDo(request):
    if request.method == 'POST':
        form = CreateToDoForm(request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, f'La Tarea quedo agendada!')
            return redirect('homePage')
    else:
        form = CreateToDoForm()
    context = {"title": "Crear Tarea", 'form': form}
    return render(request, "compras/createToDo.html", context)


def updateToDo(request, pk):
    objToDo = ToDo.objects.get(id=pk)
    if request.method == 'POST':
        form = CreateToDoForm(request.POST, instance=objToDo)
        if form.is_valid:
            form.save()
            return redirect('homePage')
    else:
        form = CreateToDoForm(instance=objToDo)
    context = {"title": "Editar Tarea", 'form': form}
    return render(request, "compras/updateToDo.html", context)


def deleteToDo(request, pk):
    objToDo = ToDo.objects.get(id=pk)
    objToDo.delete()
    return redirect('homePage')


# BUY
def createBuy(request):
    if request.method == 'POST':
        form = CreateBuyForm(request.POST)
        if form.is_valid:
            dataForm = form.save(commit=False)
            dataForm.status = True
            dataForm.save()
            messages.success(request, f'La compra quedo agendada!')
            return redirect('homePage')
    else:
        form = CreateBuyForm()
    context = {"title": "Crear Compra", 'form': form}
    return render(request, "compras/createBuy.html", context)


def updateBuy(request, pk):
    buyObj = Buy.objects.get(id=pk)
    if request.method == 'POST':
        form = CreateBuyForm(request.POST, instance=buyObj)
        if form.is_valid:
            dataForm = form.save(commit=False)
            dataForm.status = True
            dataForm.save()
            messages.success(request, f'Modificacion exitosa!')
            return redirect('homePage')
    else:
        form = CreateBuyForm(instance=buyObj)
    context = {"title": "Editar Compra", 'form': form}
    return render(request, "compras/updateBuy.html", context)


def deleteBuy(request, pk):
    buyObj = Buy.objects.get(id=pk)
    buyObj.delete()
    return redirect('homePage')


def historyBuy(request):
    history = Buy.objects.filter(status='False')
    context = {"title": "My Home", 'history': history}
    return render(request, 'compras/historyBuy.html', context)


def historyReactivate(request, pk):
    buyObj = Buy.objects.get(id=pk)
    buyObj.status = True
    buyObj.save()
    return redirect('homePage')


def closeBuy(request):
    objBuy = Buy.objects.filter(status='True')
    currentdate = pd.Timestamp.today().strftime('%Y-%m-%d')
    if not objBuy:
        messages.success(request, f'No Items en la lista!')
    else:
        #excel
        wb = Workbook()
        ws = wb.active
        ws.title = "Compras"
        for item in objBuy:
            item.status = False
            item.dateEnd = datetime.datetime.now()
            ws.append([item.id, item.toBuy, item.dateStart])
            item.save()
        wb.save("compras/templates/compras/mail/compras.xlsx")

        #email
        email_to = "masutier@gmail.com"
        html = '''
            <html>
                <body>
                    <h3>List of Items to buy</h3>
                </body>
            </html>
            '''
        email_message = MIMEMultipart()
        email_message['from'] = settings.EMAIL_HOST_USER
        email_message['to'] = email_to
        email_message['subject'] = f'Report email - {currentdate}'
        email_message.attach(MIMEText(html, "html"))
        attach_file_to_mail(email_message, "compras//templates/compras/mail/compras.xlsx")
        email_string = email_message.as_string()
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, email_to, email_string)
        messages.success(request, f'Email was sent!')

    return redirect('homePage')


def attach_file_to_mail(email_message, filename):
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename = {filename}",
    )
    email_message.attach(file_attachment)
