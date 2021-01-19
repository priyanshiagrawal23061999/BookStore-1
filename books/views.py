from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from books.models import *
import os
from book_store import settings

from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate, login, logout

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


UserModel = get_user_model()
from .forms import RegisterForm
from .token_generator import account_activation_token
from .decorators import unauthenticated_user,admin_only,allowed_users

def index(request):
    template = loader.get_template('index.html')
    context = {'tfmess': 'False'}
    context['cateobj'] = cateobj = Cate.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.user.is_authenticated:
        umail = request.user.email
        context['tfmess'] = 'True'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id

    return HttpResponse(template.render(context,request))
        
@unauthenticated_user
def loginpage(request):
    print('login',request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        user = authenticate(request, username=username, password=password)
        print(user)
        # user2 = requests.post('http://127.0.0.1:8000//login/token/',
        #                       data={'username': username, 'password': password})
        # print('user2', user2)
        if user is not None:
            login(request,user)
            return redirect('index')

        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'Auth/login.html', context)

def logoutpage(request):
    print('request',request)
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'GET':
        return render(request, 'Auth/register.html')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # print(form.errors.as_data())
        if form.is_valid():
            print('Valid')
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('Auth/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            print(to_email)
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            print(message,'message')
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            print('invalid')
    else:
        form = SignUpForm()
    return render(request, 'Auth/register.html', {'form': form})

def activate(request, uidb64, token):
    print("Activated")
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def search(request):
    template = loader.get_template('search.html')
    context = {'mess': "",'tfmess': 'False'}
    nnn = ''
    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.method == 'POST':
        context['sval'] = sval = (request.POST.get('sval')).title()

        for x in bobj:
            if x.book_author == sval or x.book_genre == sval or x.book_title == sval or x.book_publisher == sval:
                nnn = 'True'

        if nnn == '':
            context['mess'] = 'Results not found'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

def cate(request, prod_id):
    template = loader.get_template('cate.html')
    context = {'mess': "",'tfmess': 'False'}
    val = 0

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'


    context['cn'] = cn = Cate.objects.get(id=prod_id)

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    for x in bobj:
        if x.book_genre == cn.cate_name:
            val = 1

    if val == 0:
        context['mess'] = 'No books Available'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

def sprod(request, prod_id):
    template = loader.get_template('singleproduct.html')
    context = {'mess': "single",'tfmess': 'False'}
    request.session['bid'] = None

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    context['cn'] = cn = Books.objects.get(id=prod_id)
    request.session['bid'] = cn.id

    context['cobj'] = cobj = Cate.objects.all()
    context['bobj'] = bobj = Books.objects.all()
    context['bcobj'] = bcobj = Bcomm.objects.all()

    if request.method == 'POST':
        ctext = request.POST.get('ctext')
        obj = Bcomm.objects.create(btitle=cn.book_title, bcom=ctext, bumail=umail)
        obj.save()
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))



#--------------------- provider -------------------

def pro_home(request):
    template = loader.get_template('provider/pro_home.html')
    context = {'mess': ""}

    uobjmail = request.session['umail']
    context['bobj'] = bobj = Books.objects.all()
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

def pro_add_book(request):
    template = loader.get_template('provider/pro_add_book.html')
    context = {'mess': ""}
    uobjmail = request.session['umail']

    if request.method == 'POST':
        context['val'] = 'no'
        title = (request.POST.get('btitle')).title()
        genre =(request.POST.get('bgenre'))
        isbn =(request.POST.get('bisbn'))
        author =(request.POST.get('bauthor')).title()
        publisher =(request.POST.get('bpub')).title()
        copies =(request.POST.get('bcopies'))
        price =(request.POST.get('bprice'))
        lang =(request.POST.get('blang')).title()
        year =(request.POST.get('byear'))
        desc =(request.POST.get('bdes'))
        fupload = request.FILES['bphoto']


        upobj = Books.objects.create(
            book_title=title,
            book_author=author,
            book_copies=copies,
            book_description=desc,
            book_image=fupload,
            book_isbn10=isbn,
            book_pmail=uobjmail,
            book_year=year,
            book_publisher=publisher,
            book_price=price,
            book_lang=lang,
            book_genre=genre
        )
        upobj.save()
        context['mess'] = 'Book added Successfully'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))


def pro_report(request):
    template = loader.get_template('provider/pro_reports.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()


    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

#--------------------- customer -------------------
@login_required(login_url='login')
def cart0(request):
    template = loader.get_template('cart0.html')
    context = {'mess': "single", 'tot': '', 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

        if request.session.has_key('bid'):
            context['bid'] = bid = request.session['bid']

            for x in Books.objects.all():
                if x.id == bid:
                    tit = x.book_title

            cmobj = Cart.objects.create(
                cbid=bid,
                cbtitle=tit,
                cbmail=umail
            )

            cmobj.save()

            return redirect('cart')
    else:
        return redirect('login')

@login_required(login_url='login')
def cart(request):
    template = loader.get_template('cart.html')
    context = {'mess': "", 'tot':0, 'tfmess': 'False'}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

        context['addr'] = addr = Ureg.objects.get(umail=umail)

        for b in bobj:
            for c in cobj:
                if c.cbtitle == b.book_title and c.cstat == 'no':
                    context['tot'] += int(b.book_price)

        if request.method == 'POST':
            uobj = Ureg.objects.get(umail=umail)
            caddr1 = request.POST.get('caddr1')
            caddr2 = request.POST.get('caddr2')
            rval = request.POST.get('eradio')

            for b in bobj:
                for c in cobj:
                    if c.cbtitle == b.book_title and c.cstat == 'no':
                        c.cstat = 'yes'
                        b.book_copies -= 1
                        b.save()
                        c.save()

            context['tot'] = 0

            if rval == 'eval':
                uobj.save()
                context['mess'] = 'Orders placed successfully, please check for reports'

            if rval == 'nval':
                if caddr2 != '' or caddr2 != None:
                    uobj.uaddr = caddr2
                    uobj.save()
                    context['mess'] = 'Orders placed successfully, please check for reports'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def orders(request):
    template = loader.get_template('orders.html')
    context = {'mess': "single", 'tfmess': 'False'}

    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'


    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

@login_required(login_url='login')
def account(request):
    template = loader.get_template('account.html')
    context = {'mess': "", 'tfmess': 'False'}
    username = request.user.username
    context['tfmess'] = 'True'
    print(UserModel.objects.get(username=username))
    context['uobj'] = uobj = UserModel.objects.get(username=username)

    if request.method == 'POST':

        uuobj = UserModel.objects.get(id=uobj.id)

        uuobj.upass = request.POST.get('upass')
        uuobj.ufname = request.POST.get('ufname')
        uuobj.usname = request.POST.get('usname')
        uuobj.uaddr = request.POST.get('uaddr')
        uuobj.uphone = request.POST.get('uphone')
        uuobj.ucard = request.POST.get('ucard')

        uuobj.save()

        context['mess'] = 'Account Details Updated'
    # result = go_to_sleep.delay(1)
    # context['task_id']= result.task_id
    return HttpResponse(template.render(context, request))

