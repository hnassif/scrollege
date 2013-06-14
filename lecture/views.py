# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
# from djagno.template import loader
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
# from lecture.models import Session, SessionTransaction, Question
# import simplejson

from django.contrib.auth.decorators import login_required

from forms import RegForm, SignInForm, ItemForm
from models import Item


def showItems(request):
    q = Item.objects.all()
    return render_to_response('display.html', {'items': q, 'user': request.user})


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    email = password = ''
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['signin_email']
            password = form.cleaned_data['password']
            # hack to use emails only
            user = authenticate(username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    form.addError(
                        "Your account is not active, please contact the site admin.")
            else:
                form.addError("Your email and/or password were incorrect.")
    else:
        # register
        form = SignInForm()
# return render_to_response('auth.html',{'state':state, 'username':
# username})
    return render_to_response(
        'sign_in.html',
        {
            'form': form,
            'user': request.user
        },
        context_instance=RequestContext(request)
    )


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def savingItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            Item(
                item_name=form.cleaned_data['item_name'],
                item_type=form.cleaned_data['item_type'],
                item_image=request.FILES['item_image'],
                item_owner=request.user,
                item_description=form.cleaned_data['item_description'],
            ).save()

    else:
        form = ItemForm()
    return render_to_response('frontpage.html', {'form': form, 'user': request.user}, context_instance=RequestContext(request))


def home(request):
    if request.user.is_authenticated():
        return savingItem(request)
    else:
        return render_to_response('homepage.html',
                                  {'user': request.user})


def register(request):
    if request.user.is_authenticated():
        return savingItem(request)
    user = None
    signinform = SignInForm()
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            user = User(
                first_name=form.cleaned_data['firstname'],
                last_name=form.cleaned_data['lastname'],
                email=form.cleaned_data['email'],
                username=form.cleaned_data['email']
            )
            user.set_password(form.cleaned_data['password1'])
            try:
                user.save()
            except IntegrityError:
                form.addError(user.email + ' is already a member')
            else:
                user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                return HttpResponseRedirect('/')
    else:
        form = RegForm()
    return render_to_response(
        'register.html',
        {
        'form': form,
        'signinform': signinform,
        'months': range(1, 12),
        'user': request.user,
        },
        context_instance=RequestContext(request)
    )

#@login_required(redirect_field_name='/')
# def choose_class(request):
#
