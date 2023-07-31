from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.contrib.auth import logout, login, authenticate, get_user_model, get_user
from accounts.models import Person
from .forms import *


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
    if request.POST:
        errors_list = {}
        labels = {
            'username': "Nom d'utilisateur",
            'first_name': 'Prenom',
            'last_name': 'Nom',
            'country': 'Pays',
            'city': 'Ville',
            'location': 'Adresse',
            'email': 'Email',
            'phone_number': 'Numero de téléphone',
            'password': 'Mot de passe',
            }
        print('request post')
        name_to_validate = request.POST.get('username')
        if name_to_validate:
            print('validation')
            exist_persons = Person.objects.filter(username__contains=name_to_validate)
            if exist_persons.count() > 0:
                print("person's count > 0" )
                print('form invalid 1')
                context = {
                "error": True,
                "error_message": "Un utilisateur ayant le même nom existe déjà !"
                }
                return render(request, 'response.html', context)
            else:
                print("person's count == 0" )

                form = PersonForm(request.POST, request.FILES)
                for x, y in labels.items():
                    if not request.POST.get(x):
                        # print(x)
                        errors_list.update({x: y})
                print('error_list: ' ,errors_list)
                if len(errors_list) == 0:
                    print('error_list: == 0')
                    if form.is_valid():
                        print('form valid')
                        #form.save()
                        username = request.POST.get('username')
                        password = request.POST.get('password')
                        # user = authenticate(username=username, password=password)
                        # login(request, user)
                        # return redirect(reverse_lazy('home'))
                        context = {
                            'url': reverse('login'),
                            'success': True,
                            'name': 'username',
                            'success_message': 'Vous avez été correctement enregistré !'
                        }
                        return render(request, 'response.html', context)
                    else:
                        print('form invalid 2')
                        errors = form.errors
                        for key, value in labels.items():
                            if key in errors:
                                errors_list.update({key: value})
                        context = {
                        "errors_list": errors_list,
                        "error": True,
                        "error_message": "Les éléments suivants sont nécessaires :",
                        'url': reverse('signup'),
                        'form': form,
                        }
                        return render(request, 'response.html', context)
                else:
                    print('error_list: != 0')

                    print('form invalid 3')
                    errors = form.errors

                    for key, value in labels.items():
                        if key in errors:
                            errors_list.update({key: value})

                    context = {
                    "errors_list": errors_list,
                    "error": True,
                    "error_message": "Les éléments suivants sont nécessaires :",
                    'url': reverse('signup'),
                    }
                    return render(request, 'response.html', context)
        
        else:
            print('nothing to validate')
            print('form invalid 4')
            context = {
                    "errors_list": {"username": "Nom d'utilisateur"},
                    "error": True,
                    "error_message": "Les éléments suivants sont nécessaires :",
                    'url': reverse('signup'),
                    }
            # print('reverse :', reverse('signup'))
            return render(request, 'response.html', context)
        
    return render(request, 'signup.html', {'dateform': JoinedDate()})


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
