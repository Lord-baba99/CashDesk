from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate, get_user_model, get_user
from accounts.models import Person


User = get_user_model()


def logout_user(request):
    logout(request)
    return redirect('login')


def login_user(request):
    global url
    if request.method == 'GET':
        url = request.GET.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if url:
                return redirect(f'{url}')
            elif not url:
                return redirect('home')
        elif user==None:
            return render(request, 'login.html', {'error_message': 'Nom d\'utilisateur ou mot de passe invalide !'})

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        name_to_validate = request.POST.get('username')
        exist_persons = Person.objects.filter(username__contains=name_to_validate)
        if exist_persons.count() > 0:
            context = {
            "error": True,
            "error_message": "Un utilisateur ayant le même nom existe déjà !"
            }
            return render(request, 'error.html', context)
        else:
            form = PersonForm(request.POST, request.FILES)
            
            if form.is_valid():
                if form.save():
                    username = request.POST.get('username')
                    password = request.POST.get('password')
                    user = authenticate(username=username, password=password)
                    login(request, user)
                    return redirect(reverse_lazy('home'))
            else:
                errors_list = {}
                errors = form.errors
                labels = {
                    'profile_picture': 'Photo de profile',
                    'username': "Nom d'utilisateur",
                    'first_name': 'Prenom',
                    'last_name': 'Nom',
                    'country': 'Pays',
                    'city': 'Ville',
                    'location': 'Adresse',
                    'email': 'Email',
                    'phone_number': 'Numero de téléphone',
                    'birthday': 'Date de Naissance',
                    'qualification': 'Fonction',
                    }

                for key, value in labels.items():
                    if key in errors:
                        errors_list.update({key: value})

                context = {
                "errors_list": errors_list,
                "error_message": "Les éléments suivants sont nécessaires"
                }
                return render(request, 'error.html', context)
    return render(request, 'signup.html')


def show_profile(request):
    user = request.user
    context = {
        'user': user,
    }
    return render(request, 'user_profile.html', context)


def update_profile(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        location = request.POST.get('location')
        niu = request.POST.get('niu')
        profile_picture = request.POST.get('profile_picture')
        gender = request.POST.get('gender')
        phone_number = request.POST.get('phone_number')
        driving_licence_picture = request.POST.get('driving_licence_picture')
        driving_licence_number = request.POST.get('driving_licence_number')
        id_card_picture = request.POST.get('id_card_picture')
        id_card_number = request.POST.get('id_card_number')

        requested_user = get_user(request)
        user = Person.objects.filter(id=requested_user.id)
        user.update(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            location=location,
            niu=niu,
            profile_picture=profile_picture,
            gender=gender,
            phone_number=phone_number,
            driving_licence_picture=driving_licence_picture,
            driving_licence_number=driving_licence_number,
            id_card_picture=id_card_picture,
            id_card_number=id_card_number,
        )
        return redirect('profile')
    return redirect('profile')
