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

try: import simplejson as json
except ImportError: import json

from django.contrib.auth.decorators import login_required

from forms import RegForm, SignInForm, ItemForm
from models import Item


def home(request):
    q = Item.objects.all().reverse()
    return render_to_response('homepage_default.html', {'items': q, 'user': request.user})

def my_items(request):
    list_of_my_items = Item.objects.filter(item_owner=User.objects.filter(id=request.user.id)[0])
    print list_of_my_items
    print "request.user is" + str(request.user.id)
    return render_to_response('my_items.html', {'items': list_of_my_items, 'user': request.user})

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


def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            Item(
                item_name=form.cleaned_data['item_name'],
                item_type=form.cleaned_data['item_type'],
                # item_image=request.FILES['item_image'],
                item_price=form.cleaned_data['item_price'],
                item_negotiable=form.cleaned_data['item_negotiable'],
                item_owner=request.user,
                item_description=form.cleaned_data['item_description'],
            ).save()
            return my_items(request)

    else:
        form = ItemForm()
    return render_to_response('post_item.html', {'form': form, 'user': request.user}, context_instance=RequestContext(request))



def register(request):
    if request.user.is_authenticated():
        return post_item(request)
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


def testHenry(request):
    return render_to_response(
        'newTemplateForProfile.html')
