import os.path
from django.contrib import messages
from django.contrib.auth import get_user_model, logout, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import pandas as pd
# from django.contrib import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv
from query_app.forms import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


dataset_path = os.path.join(settings.BASE_DIR, 'Models')


def compare_string(i_text, data_in_):
    corpus = [i_text.lower(), data_in_.lower()]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
    return cosine_sim


def load_model(input_string):
    file_path = pd.read_csv(os.path.join(dataset_path, 'train_data.csv'))
    # with open(os.path.join(dataset_path, 'train_data.csv'), 'r', encoding='utf-8') as file:
    #     csv_reader = csv.DictReader(file)
    #     data = list(csv_reader)
    matching_records = []
    # code
    for row in data:
        sim_embedding = compare_string(input_string, row['docstring'])
        print(sim_embedding)
        if sim_embedding > settings.EMBED_VALUES:
            predict_res = {
                'docstring': row['docstring'],
                'code': row['code'],
                'vector': sim_embedding
            }
            matching_records.append(predict_res)
    return matching_records


# Create your views here.
def index(request):
    return render(request, "index.html")


@login_required(login_url='login')
def about(request):
    return render(request, "about.html")


@login_required(login_url='login')
def service(request):
    context = {}
    query_form = InsertQueryForm()

    context['query_form'] = query_form
    return render(request, "service.html", context)


@login_required(login_url='login')
def contact(request):
    return render(request, "contact.html")


class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None


# @login_required(login_url='login')
# def insert_url(request):
#     context = {}
#     reg_form = RegistrationForm()
#     if request.method == 'POST':
#         reg_form = RegistrationForm(request.POST)
#         if reg_form.is_valid():
#             reg = reg_form.save(commit=False)
#             password = reg.password
#             reg.set_password(password)
#             reg.save()
#             messages.info(request, 'Please confirm your email address to complete the registration')
#             return HttpResponseRedirect(reverse('index'))
#         else:
#             # context['teacher_form_error'] = 'True'
#             messages.error(request, "ERROR! while saving info please try again")
#     context['reg_form'] = reg_form
#     context['current_page'] = 'signup'
#     return render(request, 'insert-url.html', context)

def signup(request):
    context = {}
    reg_form = RegistrationForm()
    if request.method == 'POST':
        reg_form = RegistrationForm(request.POST)
        if reg_form.is_valid():
            reg = reg_form.save(commit=False)
            password = reg.password
            reg.set_password(password)
            reg.save()
            messages.info(request, 'Please confirm your email address to complete the registration')
            return HttpResponseRedirect(reverse('index'))
        else:
            # context['teacher_form_error'] = 'True'
            messages.error(request, "ERROR! while saving info please try again")
    context['reg_form'] = reg_form
    context['current_page'] = 'signup'
    return render(request, 'signup.html', context)


def login_page(request):
    context = {}
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('email')

            password = login_form.cleaned_data.get('password')
            user = EmailBackend.authenticate(request, username=username, password=password)
            if user is not None:
                print("Login Success")

                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                context['login_form_error'] = 'True'
                messages.error(request, 'Login credential not matched, please try valid credential.')
        else:
            context['login_form_error'] = 'True'
            messages.error(request, "ERROR! while saving info please try again")
    else:
        context['login_form_error'] = 'True'
    context['login_form'] = login_form
    # context['current_page'] = 'login'
    return render(request, 'login.html', context)


@login_required(login_url='login')
def Results(request):
    context = {}
    search_form = InsertQueryForm()
    if request.method == 'POST':
        search_form = InsertQueryForm(request.POST)
        if search_form.is_valid():
            input_query = search_form.cleaned_data.get('input_text')
            data = load_model(input_query)
            print(data)
            return HttpResponseRedirect(reverse('index'))
        else:
            results = None
    context['query_form'] = search_form
    return render(request, 'Results.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


# @login_required(login_url='login')
def index(request):
    return render(request, 'index.html')
