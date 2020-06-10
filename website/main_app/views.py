from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import ContactForm
from .models import contact
from django.contrib.auth.models import User
from .SmsSender import sendSms
from .Scraper import news_fetch, write_news
from os import getcwd
from .mail import send_mail
import sys
from sys import platform


# Create your views here.
def home(request):
    context = {

    }
    return render(request, 'main_app/home.html', context)


def women_rights(request):
    return render(request, 'main_app/women_rights.html', {'title': 'women_rights'})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"New Account Created Successfully: {username}")
            login(request, user)
            messages.info(request, f"Logged in as {username}")
            return redirect('main_app:home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: form.error_messages[msg]")

    form = UserCreationForm
    return render(request, 'main_app/register.html', context={'form': form})


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main_app:home")


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Successfully logged in as {username} !")
                return redirect("main_app:home")
            else:
                messages.error(request, f"Invalid username or password {username} ")
        else:
            messages.error(request, "Invausername or password  ")

    form = AuthenticationForm
    return render(request, "main_app/login.html", {'form': form})

# @login_required(login_url='login/')
def emergency_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr==0:
        return redirect("main_app:login")
    user = curr
    contacts = contact.objects.filter(user=user)
    total_contacts = contacts.count()
    context = {'contacts': contacts, 'total_contacts': total_contacts, 'user':user}

    return render(request, 'main_app/emergency_contact.html', context)


def create_contact(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    inst = contact(user=curr)
    form = ContactForm(instance=inst)
    if request.method == 'POST':
        form = ContactForm(request.POST, instance=inst)
        if form.is_valid():
            form.save()
            messages.info(request, f"New contact created successfully!!")
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('email')
            message = "Hello, " + name + "\nYour contact information has been saved as emergency contact by " + curr.username + "."
            send_mail(mail, message)
            messages.info(request, f"An email has been sent to your contact!!")
            return redirect('main_app:emergency_contact')

        messages.error(request, f"Invalid username or password")
    # messages.error(request, f"Invalid contact!!")
    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def update_contact(request, pk):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break

    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    form = ContactForm

    if request.method == 'POST':
        form = ContactForm(request.POST, instance=curr_contact)
        if form.is_valid():
            form.save()
            messages.error(request, f"{name} updated successfully!!")
            name = form.cleaned_data.get('name')
            mail = form.cleaned_data.get('email')
            message = "Hello, " + name + "\nYour contact information as emergency contact by " + curr.username + " has been updated."
            send_mail(mail, message)
            messages.info(request, f"An email has been sent to your contact!!")

            return redirect('main_app:emergency_contact')

    context = {'form': form}
    return render(request, 'main_app/create_contact.html', context)


def delete_contact(request, pk):
    curr_contact = contact.objects.get(id=pk)
    name = curr_contact.name
    if request.method == "POST":
        curr_contact.delete()
        messages.error(request, f"{name} deleted successfully!!")
        return redirect('main_app:emergency_contact')

    context = {'item': curr_contact}
    return render(request, 'main_app/delete_contact.html', context)

def emergency(request):
    users = User.objects.all()
    curr = 0
    for user in users:
        if request.user.is_authenticated:
            curr = user
            break
    if curr==0:
        return redirect("main_app:login")
    user = curr
    contacts = contact.objects.filter(user=user)
    emails = []
    for j in contacts:
        emails.append(j._meta.get_field("email"))
    name = user.username
    message = name+" is in emergency situation and need your help immediately!!"

    errors = ""
    try:
        sendSms("8350815015", message)
    except:
        errors += "Message not send to 8350815015"
        pass
    try:
        sendSms("7696043017", message)
    except:
        errors += "Message not send to 7696043017"
        pass

    for c in contacts:
        send_mail(c.email, message)

    admin = [["Parikh", "8350815015"], ["Ankit", "1234567890"]]
    context = {'contacts':contacts, 'admin':admin, 'error':errors, 'emails':emails}

    return render(request, 'main_app/emergency.html', context)


def news(request):
    if platform == "linux" or platform == "linux2":
        news_fetch()
        write_news()
    return render(request, 'main_app/news.html', {'title':'news'} )

def corona_updates(request):
    return render(request, 'main_app/corona_updates.html', {'title':'corona_updates'})

def city_map(request):
    return render(request, 'main_app/city_map.html', {'title':'city_map'})

def find_me(request):
    return render(request, 'main_app/find_me.html', {'title':'current location'})

def women_laws(request):
    return render(request, 'main_app/women_laws.html', {'title': 'women_laws'})

def helpline_numbers(request):
    return render(request, 'main_app/helpline_numbers.html', {'title': 'helpline_numbers'})

def developers(request):
    return render(request, 'main_app/developers.html', {'title': 'developers'})