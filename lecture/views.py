# Create your views here.
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect, render
from django.template import RequestContext
# from djagno.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
#from lecture.models import Session, SessionTransaction, Question
import simplejson
from django.contrib.auth.decorators import login_required

from forms import RegForm, SignInForm, ItemForm
from models import Item


def showItems(request):
	q=Item.objects.all()
	return render_to_response('display.html',{'items':q})


def sign_in(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    username = password = ''
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
            		item = Item(
                		item_name= form.cleaned_data['item_name'],
				item_type=form.cleaned_data['item_type'],
				item_image=request.FILES['item_image'],
				item_owner=request.user,
				item_description= form.cleaned_data['item_description'],
            			).save()

	else:
		form=ItemForm()
        return render_to_response('frontpage.html',{'form':form},context_instance=RequestContext(request))


def home(request):
    if request.user.is_authenticated():
        savingItem(request)
    else:
        return render_to_response('homepage.html')

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
        'user': user,
        },
        context_instance=RequestContext(request)
    )

#@login_required(redirect_field_name='/')
# def choose_class(request):
#

"""
def session_or_new():
    s = Session.objects.all()
    if s:
        return s[0]
    else:
        n_sess = Session()
        n_sess.save()
        return n_sess


def post_data(request):
    session = request.session.get('lec_session')
    if session is None:
        s = session_or_new()
        request.session['lec_session'] = s.pk
    s_obj = Session.objects.get(pk=request.session.get('lec_session'))
    if request.method == 'GET':
#        f = open('/tmp/workfile', 'a')
#        f.write(str(request.session)+'\n')
        if request.GET['button'] == 'slow_down':
            SessionTransaction(
                too_fast=True,
                session=s_obj
            ).save()
            return HttpResponse('OK', status=200)
        if request.GET['button'] == 'lost':
            SessionTransaction(
                lost=True,
                session=s_obj
            ).save()
            return HttpResponse('OK', status=200)
        if request.GET['button'] == 'speed_up':
            SessionTransaction(
                too_slow=True,
                session=s_obj
            ).save()
            return HttpResponse('OK', status=200)
        if request.GET['button'] == 'question':
            pass
    else:
        return HttpResponse(request.GET['button'] + "Server REPLY :D.", status=200)
    return HttpResponse(request.GET['button'] + "Server REPLY :D.", status=200)


def stream(request):
#    return HttpResponse('asdf');
    return render_to_response('stream.html',
                              {'page': 'stream', 'haha': 'haha'},
                              context_instance=RequestContext(request))
#    render(request,'stream.html')


def stream_qn(request):
    try:
        if 'initial' in request.GET:
            query = Question.objects.order_by('-timestamp')[:20]
            msg = []
            for x in query:
                msg.append({'id': x.pk,
                            'question': x.qn})
            return HttpResponse(simplejson.dumps(msg), status=200,
                                mimetype='application/json'
                                )
        else:
            n = Question.objects.order_by('-timestamp')[:1][0]
            return HttpResponse(simplejson.dumps({
                                                 'id': n.pk,
                                                 'question': n.qn}),
                                mimetype='application/json')
    except:
        return HttpResponse('ERROR', status=400)


def prof_graph(request):
    return render_to_response('prof.html')


def graph_data(request):
#    try:
        if 'latest' in request.GET:
            l = SessionTransaction.objects.order_by('-timestamp')[:1][0]
            dict = {'id': l.id}
            return HttpResponse(simplejson.dumps(dict), status=200, mimetype='application/json')
        else:
            curr = request.GET['id']
            q = SessionTransaction.objects.all().filter(pk__gt=int(curr))
            li = []
            for x in q:
                li.append({'id': x.id,
                           'too_fast': x.too_fast,
                           'too_slow': x.too_slow,
                           'lost': x.lost})
            return HttpResponse(simplejson.dumps(li), status=200, mimetype='application/json')
#    except:
#        return HttpResponse('ERROR',status=300)


def session_stats(request):
    session = request.session.get('lec_session')
    if session is None:
        s = session_or_new()
        session = s.pk
        request.session['lec_session'] = session
    s = Session.objects.get(pk=session)
    s_trans = SessionTransaction.objects.all().filter(session=s)
    tfast = tslow = lost = 0
    for x in s_trans:
        if x.lost:
            lost += 1
        elif x.too_fast:
            tfast += 1
        elif x.too_slow:
            tslow += 1
    check = True if (tfast + tslow + lost) == len(s_trans) else False
    dict = {'too_fast': tfast,
            'too_slow': tslow,
            'lost': lost,
            'check': check}
    return HttpResponse(simplejson.dumps(dict), status=200, mimetype='application/json')
#    else:
#        dict = {'too_fast':0,
#                'too_slow' : 0,
#                'lost': 0,
#                'check':False}
# return HttpResponse(simplejson.dumps(dict), mimetype='application/json')


def rec_qn(request):
    # TODO:login required
    session = request.session.get('lec_session')
    if session is None:
        s = session_or_new()
        session = s.pk
        request.session['lec_session'] = session
    s = Session.objects.get(pk=session)
    if request.GET['question']:
        user = None
        if request.user.is_authenticated():
            q = Question(
                student=request.user,
                session=s,
                qn=str(request.GET['question']))
        else:
            q = Question(
                session=s,
                qn=str(request.GET['question']))
        q.save()
        return HttpResponse('OK')
    else:
        return HttpResponse('ERROR', status=400)


"""
