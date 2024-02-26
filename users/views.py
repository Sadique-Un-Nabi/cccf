from django.contrib import messages
from django.contrib.auth import login, get_user_model, authenticate
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.files import File

from .models import Profile
from datetime import datetime
from .py_funcs import ccis_info, extract_college_name

from tempfile import NamedTemporaryFile
import requests
from PIL import Image
from io import BytesIO


@csrf_protect
def register_view(request):

    if request.method == 'POST':
        

        user_id = request.POST.get('user_id')
        password = request.POST.get('password')
        print(request.POST)

        #if CustomUser.objects.get(username=user_id)

        cadet_info = ccis_info(user_id, password)
        print(cadet_info)

        if cadet_info:
            # Get the user model specified in settings.py
            User = get_user_model()

            user = User(username=user_id)
            # Set the user's password
            user.set_password(password)

            # Save the user object to the database
            user.save()




            profile = Profile(user=user)
            
            # Create a new user object and populate its fields
            profile = Profile(
                user=user,
                gender='F' if 'G' in user_id else 'M',  # Determine gender based on username
                date_of_birth=cadet_info['date_of_birth'],  # Set date of birth
                intake=cadet_info['intake'],  # Set intake
                cadet_name=cadet_info['cadet_name'],
                college_name=extract_college_name(user_id),
                full_name=cadet_info['full_name'],
            )
            print(cadet_info)

            response = cadet_info['image_data']
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                img_temp = NamedTemporaryFile(delete=True, suffix=".webp")
                image.save(img_temp, "WEBP")
                img_temp.flush()
                profile.image.save(f'{user.username}/{user.username}.webp', File(img_temp))
            


            # Log the user in after successful registration
            login(request, user)

            return redirect(profile.get_absolute_url())
        else:
            messages.error(request, 'Invalid form data')

    return render(request, 'users/register.html')

def login_view(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=user_id, password=password)
        
        if user is not None:
            # Log the user in if authentication is successful
            login(request, user)
            return redirect(user.profile.get_absolute_url())
        else:
            # Might wanna render a custom error page.
            return render(request, 'users/login.html', {"error_msg":"Invalid Username or Password"})

    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')
