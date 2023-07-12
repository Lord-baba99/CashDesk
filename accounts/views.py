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
        print(username, password)
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

        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')

            user = User.objects.create_user(
                password=password,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            login(request, user)
            return redirect(reverse_lazy('profile'), context={'user': user})

        except IntegrityError:
            context = {
                'user_exist': True,
                'username': name_to_validate,
                       }
            return render(request, 'signup.html', context)
    context = {

    }
    return render(request, 'profile.html', context)


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
