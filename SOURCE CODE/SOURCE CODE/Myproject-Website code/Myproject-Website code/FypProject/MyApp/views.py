from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Hotels, Type, Comment
from .forms import *
from django.db.models import Avg
from django.db.models import Func
from django.conf import settings
from django.core.mail import send_mail
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
import joblib
from tensorflow.keras.models import load_model
from tensorflow.python.keras import backend as k
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Profile
import uuid
from django.conf import settings
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
# Create your views here.
#
# model = load_model(r'‪‪C:\Users\DELL\sentiment.h5')
# tokenizer = joblib.load(r'C:\Users\DELL\tokenizer.pkl')
import pickle
import numpy as np
import tensorflow as tf
import joblib

import h5py

# loaded_model = tf.keras.models.load_model(r'‪F:\Program\Python\sentiment.h5')
from keras.models import load_model

model = load_model('D:/hotelrecommendation/SOURCE CODE/SOURCE CODE/Aimodel/Aimodel/sentiment.h5')
loaded_model1 = joblib.load('D:/hotelrecommendation/SOURCE CODE/SOURCE CODE/Aimodel/Aimodel/tokenizer.pkl')



def home(request):
    obj = Hotels.objects.all()
    context = {

        'object': obj
    }
    return render(request, 'MyApp/Home.html',context)


def login_try(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
       
        user = User.objects.filter(username= username).first()
        if user is None:
            messages.success(request, 'User not found please try again.')
            return redirect('login_try')
        try:
            profile = Profile.objects.filter(user=user).first()
            if not profile.is_verified:
                messages.success(request, 'Profile is not verified check your mail.')
                return redirect ('login_try')
        except:
            print("profile doesnot exist for user")

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Your password is invalid please try again.')
            return redirect('login_try')

        login(request, user)
        return redirect('home')

    return render(request, 'MyApp/Login.html')

#old
    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = auth.authenticate(username=username, password=password)

    #     if user is not None:
    #         auth.login(request, user)
    #         return redirect("home")

    #     else:
    #         messages.info(request, 'Invalid input or Not verified!')
    #         return redirect('login')
    # else:
    #     return render(request, 'MyApp/login.html')


def about(request):
    return render(request, 'MyApp/about.html')


def register(request):

    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
    
        if User.objects.filter(username=username).exists():
            messages.info(request,'Username Already Taken!')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email Already Taken!')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username,  email=email, password=password, first_name=first_name, last_name=last_name)
            user.save()
            auth_token = str(uuid.uuid4())
            profile = Profile.objects.create(user = user, auth_token =  auth_token)
            profile.save()
            send_mail_registration(email, auth_token)
            print('user created') 
            return redirect('/token')

    else:
        return render(request, 'MyApp/register.html')

def success(request):
    return render(request, 'MyApp/success.html')

def token_send(request):
    return render(request, 'MyApp/token_send.html')

def verify(request, auth_token):
    try:
        profile = Profile.objects.filter(auth_token = auth_token).first()
        if profile:
            if profile.is_verified:
                messages.success(request, 'Your account is already verified') 
                return redirect('/login')  
            profile.is_verified = True
            profile.save()
            messages.success(request, 'Your account has been verified')
            return redirect('/login')  
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return render(request, 'MyApp/error.html')

def logout(request):
    auth.logout(request)
    return redirect('home')


def types(request):
    obj = Type.objects.all()

    context = {
        'object': obj
    }
    return render(request, 'MyApp/types.html', context)


def hotel_types(request, id):
    type = Type.objects.get(id=id).types.all()
    context = {

        'types': type
    }
    return render(request, 'MyApp/allhotels.html', context)


def hotel_info(request, id):
    information = Hotels.objects.get(id=id)
    comments = Comment.objects.filter(hotels=information).order_by('-id')
    rating = 0.0
    class Round(Func):
        function = 'ROUND'
        arity = 2


    if (comments.count() > 0):
        rating = comments.aggregate(rounded_avg=Round(Avg('rating'), 1.0))

    if request.method == "POST":
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            content = request.POST.get('content')
            txt = content
            seq = np.array([txt])
            seq = loaded_model1.texts_to_sequences(seq)
            txt = tf.keras.preprocessing.sequence.pad_sequences(seq, maxlen=130)
           
            score = model.predict(txt)
            predict = np.argmax(score, axis=1)
            # model.predict_classes(txt)
            print(predict)
            print(score)
            if(score >0.90):
                rating = 5
            elif(score >0.85 and score <0.89):
                rating = 4
            elif(score > 0.75 and score < 0.84):
                rating = 3
            elif(score > 0.73 and score < 0.74):
                rating = 2
            else:
                rating = 1
    
            comment = Comment.objects.create(hotels=information, rating=rating, user=request.user, content=content)
            comment.save()

            return HttpResponseRedirect('/info/(%s)/' % id)

    else:
        comment_form = CommentForm()

    is_favourite = False
    if information.favourite.filter(id=request.user.id).exists():
        is_favourite = True

    context = {

        'is_favourite': is_favourite,
        'info': information,
        'comments': comments,
        'comment_form': comment_form,
        'rating': rating,
    }
    return render(request, 'MyApp/info.html', context)


def search(request):
    query = request.GET.get('q')
    obj = Hotels.objects.all().prefetch_related('types')
    results = obj.filter(Q(name__icontains=query) |Q(types__Rname__icontains=query) )

    context = {
        'types':results
    }
    return render(request,'MyApp/allhotels.html',context)


def favourite(request, id):
    hotel = get_object_or_404(Hotels, id=id)
    if hotel.favourite.filter(id=request.user.id).exists():
        hotel.favourite.remove(request.user)
    else:
        hotel.favourite.add(request.user)
    return HttpResponseRedirect('/info/(%s)/' %id)


def favourite_list(request):
    user = request.user
    favourites = user.favourite.all()
    context = {
        'types': favourites
    }
    return render(request, 'MyApp/allhotels.html', context)

def send_mail_registration(email, token):
    subject = 'Your accounts need to be verefied'
    message = f'Hi Paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from,recipient_list)
