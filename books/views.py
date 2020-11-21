from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from books.models import *
import os
from book_store import settings
from django.core.mail import EmailMessage

def index(request):
    template = loader.get_template('index.html')
    context = {'tfmess': 'False'}
    context['cateobj'] = cateobj = Cate.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    return HttpResponse(template.render(context,request))

def login(request):
    template = loader.get_template('login.html')
    context = {'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    if request.method == 'POST':

        umail = request.POST.get('uemail')
        upass = request.POST.get('upass')

        for x in Ureg.objects.all():
            if x.umail == umail and x.upass == upass:

                request.session['umail'] = umail

                if x.utype == 'customer':

                    return redirect('index')

                if x.utype == 'provider':
                    return redirect('pro_home')

        context['message'] = "Permission denied, your mail didn't approved"

    return HttpResponse(template.render(context,request))

def reg(request):
    template = loader.get_template('register.html')
    context = {'mess': '', 'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    if request.method == 'POST':
        uname = request.POST.get('uname')
        umail = request.POST.get('umail')
        upass = request.POST.get('upass')
        ufname = request.POST.get('ufname')
        usname = request.POST.get('usname')
        uaddr = request.POST.get('uaddr')
        uphone = request.POST.get('uphone')
        ucard = request.POST.get('ucard')
        utype = 'customer'

        for x in Ureg.objects.all():
            if x.umail == umail:
                context['mess'] = 'mail id is already registered'

        if context['mess'] != 'mail id is already registered':
            ucobj = Ureg.objects.create(
                uname=uname,
                umail=umail,
                upass=upass,
                ufname=ufname,
                usname=usname,
                uaddr=uaddr,
                uphone=uphone,
                ucard=ucard,
                utype=utype
            )

            ucobj.save()

            context['mess'] = 'Registration Successful'

    return HttpResponse(template.render(context,request))

def forgot(request):
    template = loader.get_template('Auth/forgot.html')
    context = {'tfmess': 'False'}
    request.session.flush()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'

    if request.method == 'POST':
        umail = request.POST.get('umail')

        email_subject = 'Activate Your Account'
        message = render_to_string('accounts/activate_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()


    return HttpResponse(template.render(context,request))

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

    return HttpResponse(template.render(context, request))

def logout(request):
    template = loader.get_template('logout.html')
    context = {'mess': ''}

    request.session.flush()

    return redirect('index')

#--------------------- provider -------------------

def pro_home(request):
    template = loader.get_template('provider/pro_home.html')
    context = {'mess': ""}

    uobjmail = request.session['umail']
    context['bobj'] = bobj = Books.objects.all()

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
    return HttpResponse(template.render(context, request))

def pro_report(request):
    template = loader.get_template('provider/pro_reports.html')
    context = {'mess': ""}
    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()



    return HttpResponse(template.render(context, request))

#--------------------- customer -------------------

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

    return HttpResponse(template.render(context, request))

def orders(request):
    template = loader.get_template('orders.html')
    context = {'mess': "single", 'tfmess': 'False'}

    context['cobj'] = cobj = Cart.objects.all()
    context['bobj'] = bobj = Books.objects.all()

    if request.session.has_key('umail'):
        context['umail'] = umail = request.session['umail']
        context['tfmess'] = 'True'



    return HttpResponse(template.render(context, request))

def account(request):
    template = loader.get_template('account.html')
    context = {'mess': "", 'tfmess': 'False'}
    context['umail'] = umail = request.session['umail']
    context['tfmess'] = 'True'
    context['uobj'] = uobj = Ureg.objects.get(umail=umail)

    if request.method == 'POST':

        uuobj = Ureg.objects.get(id=uobj.id)

        uuobj.upass = request.POST.get('upass')
        uuobj.ufname = request.POST.get('ufname')
        uuobj.usname = request.POST.get('usname')
        uuobj.uaddr = request.POST.get('uaddr')
        uuobj.uphone = request.POST.get('uphone')
        uuobj.ucard = request.POST.get('ucard')

        uuobj.save()

        context['mess'] = 'Account Details Updated'

    return HttpResponse(template.render(context, request))

