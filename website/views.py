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
from django.core.mail import send_mail


def home(request):
    q = Item.objects.all().order_by('timestamp').reverse()
    return render_to_response('homepage_default.html', {'items': q, 'user': request.user})

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
                image_first = form.cleaned_data['image_first'],
                image_second= form.cleaned_data['image_second'],
                image_third= form.cleaned_data['image_third'],
                looking_for = True if 'True' == form.cleaned_data['item_sellOrLookFor'] else False,
                category = form.cleaned_data['item_category'],
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
            if True or form.cleaned_data['email'].find('@mit.edu')!=-1:
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
                form.addError("You did Not enter a valid MIT address")
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


def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid:
            print "search form is valid"
        raw_q = request.GET['q']
        q = raw_q.strip()
        items = Item.objects.filter(active = True).filter(name__icontains=q) | \
                Item.objects.filter(description__icontains=q)
                #  | \
                # Item.objects.filter(tags__search=q)
        return render_to_response('search_results.html', {'items':items, 'q':q, 'user':request.user})

    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def reset_password(request):
    feedback = []
    if request.method == 'POST':
        print "received password data"
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            print "form is valid"
            old_Password=form.cleaned_data['old_Password']
            new_Password=form.cleaned_data['new_Password']
            confirm_New_Password=form.cleaned_data['confirm_New_Password']
            if (new_Password == confirm_New_Password) and request.user.check_password(old_Password):
                request.user.set_password(new_Password)
                request.user.save()
                feedback.append("password has been reset.")
            else:
                feedback.append("An Error occurred.")
        else:
            feedback.append("An Error occurred.")

    form = PasswordResetForm()
    return render_to_response('myProfile.html' , {'user': request.user, 'form': form, 'feedback':feedback})


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

@csrf_exempt
def start_thead(request):
    if request.method == "POST":
        sender = request.user
        if all(key in request.POST for key in ('message','item_id')):
            # print "all is well"
            temp_item = Item.objects.filter(id=int(request.POST['item_id']))[0]

            if temp_item:
                subject = 're: '+temp_item.name
                message = request.POST['message'].strip()
                if message:
                    full_message = sender.first_name + ' '+sender.last_name+' ('+sender.email+') is interested in '\
                    +temp_item.name+' \nPlease contact them to complete the transaction.\n'\
                    +'========================begin============================='+'\n\n'+message+'\n\n'\
                    +'========================+end+============================='
                    send_mail(subject, full_message, 'mitpost-admin@mit.edu',
                                    [temp_item.owner.email], fail_silently=False)
                Message(
                    content = request.POST['message'].strip(),
                    sender = request.user,
                    receiver = temp_item.owner,
                    item = temp_item,
                    ).save();
            else:
                return HttpResponse(json.dumps({'response':'OK'}),content_type="application/json")
    return HttpResponse(json.dumps({'response':'OK'}),content_type="application/json")


def goToMyItems(request):
   list_of_my_items = Item.objects.filter(owner=request.user)
   print list_of_my_items
   print "request.user is" + str(request.user.id)
   return render_to_response('myItems.html', {'items': list_of_my_items, 'user': request.user})

def item(request, item_id):
    "returns a page for a single item"
    item = Item.objects.filter(id= int(item_id))[0]
    return render_to_response('single_item.html',{'user' : request.user, 'item':item})
