# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
# from djagno.template import loader
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
# from lecture.models import Session, SessionTransaction, Question
# import simplejson

from django.db.models import Count
import hashlib
from django.db.models import Q
from django.utils.timesince import timesince
from django.views.decorators.csrf import csrf_exempt

try: import simplejson as json
except ImportError: import json

from django.contrib.auth.decorators import login_required

from forms import RegForm, SignInForm, ItemForm, SearchForm, PasswordResetForm
from models import Item, Message


def home(request):
    q = Item.objects.all().reverse()[:20]
    return render_to_response('homepage_default.html', {'items': q, 'user': request.user})

# @login_required
# def my_items(request):
#     list_of_my_items = Item.objects.filter(owner=User.objects.filter(id=request.user.id)[0])
#     print list_of_my_items
#     print "request.user is" + str(request.user.id)
#     return render_to_response('my_items.html', {'items': list_of_my_items, 'user': request.user})

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

@login_required
def post_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST,  request.FILES)
        if form.is_valid():
            m_tags = form.cleaned_data['item_tags']
            m = Item(
                name=form.cleaned_data['item_name'],
                # type=form.cleaned_data['item_type'],
                # item_image=request.FILES['item_image'],
                image = form.cleaned_data['image'],
                price=form.cleaned_data['item_price'],
                negotiable=form.cleaned_data['item_negotiable'],
                owner=request.user,
                description=form.cleaned_data['item_description']
            )
            m.save()
            print "item has been saved with item_id "+str(m.pk)
            print m_tags
            m.tags.add(*m_tags)
            # return my_items(request)
            return HttpResponseRedirect('/')

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
 list_of_my_items = Item.objects.filter(owner=request.user)
 form = PasswordResetForm()
 print list_of_my_items
 print "request.user is" + str(request.user.id)
 return render_to_response('newTemplateForProfile.html', {'items': list_of_my_items, 'user': request.user, 'form': form})

def testDavid(request):
    form = SearchForm()
    return render_to_response('search.html',{'form':form})


def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid:
            print "search form is valid"
        raw_q = request.GET['q']
        q = raw_q.strip()
        items = Item.objects.filter(name__icontains=q) | \
                Item.objects.filter(description__icontains=q)
                #  | \
                # Item.objects.filter(tags__search=q)
        return render_to_response('search_results.html', {'items':items, 'q':q})

    else:
        return HttpResponseRedirect('/')

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            new_Password=form.cleaned_data['newPassword']
            confirm_New_Password=form.cleaned_data['confirmNewPassword']
            if new_Password == confirm_New_Password:
                request.user.set_password(newPassword)
    else:
        form = PasswordResetForm()

@login_required
def messages(request):
    if request.user.is_authenticated():
        list_of_my_messages = Message.objects.filter(item__owner=request.user)
        list_of_my_items = Item.objects.filter(owner=User.objects.filter(id=request.user.id)[0])
        print list_of_my_items
        return render_to_response('messages.html', {'items': list_of_my_items, 'messages': list_of_my_messages})
    else:
        raise Http404


# Messages JSON API
@login_required
def item_messages(request):
    # try:
        if request.method == 'GET':
            id=request.GET["id"]
            list_of_messages = Message.objects.filter(
                item__owner=request.user,item__id=id).filter(~Q(sender=request.user)).values(
                'sender','sender__first_name','sender__last_name','sender__email','item','item__name','item__price').order_by().annotate(Count('sender'))
            for x in list_of_messages:
                x['sender__email'] = hashlib.md5(x['sender__email']).hexdigest()
            # return HttpResponse(str(list(list_of_messages)));
            return HttpResponse(json.dumps(list(list_of_messages)),content_type="application/json")

@login_required
def message_thread(request):
    if request.method == 'GET':
        item_id = request.GET['item_id']
        sender_id = request.GET['sender_id']
        thread_msgs = Message.objects.filter(item_id=item_id).filter(
            (Q(sender__id=sender_id)&Q(receiver=request.user))|(Q(sender__id=request.user.id)&(Q(receiver__id=sender_id)))).values(
            'timestamp','sender__first_name','sender__last_name','sender__email','content').order_by('-timestamp')
        
        for x in thread_msgs:
            x['sender__email'] = hashlib.md5(x['sender__email']).hexdigest()
            x['timestamp'] = timesince(x['timestamp'])
        response = {'request':{'user_id':request.user.id},'data':list(thread_msgs)}
        return HttpResponse(json.dumps(response), content_type="application/json")

# def msg_from_id(request):
#     if request.method == "GET":
#         msg = Message.objects.filter(pk=request.GET["id"])[0].jOb()
#     else:
#         msg = None
#     return HttpResponse(json.dumps(msg),content_type="application/json")


# @login_required
@csrf_exempt
def send_message(request):
    if request.method == "POST":
        if all(key in request.POST for key in ('message','sender_id','item_id')):
            Message(
                content = request.POST['message'].strip(),
                sender = request.user,
                item  = Item.objects.filter(id=int(request.POST['item_id']))[0],
                # todo: check if user has contacted user initially
                receiver = User.objects.filter(id=int(request.POST['sender_id']))[0],
                isRead = False
                ).save()
        
    return HttpResponse(json.dumps(1),content_type="application/json")



def goToProfile(request):
 form = PasswordResetForm()
 return render_to_response('myProfile.html' , {'user': request.user, 'form': form})

def goToMyItems(request):
     list_of_my_items = Item.objects.filter(owner=request.user)
     print list_of_my_items
     print "request.user is" + str(request.user.id)
     return render_to_response('myItems.html', {'items': list_of_my_items, 'user': request.user})