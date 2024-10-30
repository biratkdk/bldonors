from django.shortcuts import redirect, render , HttpResponseRedirect
from .forms import Bloodreqform, Donorform , Stockform , Contactform , createuserform
from .models import Bloodreq, Donor , Stock , Contact
from django.contrib.auth import authenticate, login as dj_login , logout as dj_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "base.html")

def blog(request):
    return render(request, "blog.html")

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

#this function will add and show donor data
def donor(request):
    if request.method == 'POST':
        fm = Donorform(request.POST)
        if fm.is_valid():
          nm =  fm.cleaned_data['name']
          em =  fm.cleaned_data['email']
          ph = fm.cleaned_data['phone']
          ad = fm.cleaned_data['address']
          ag = fm.cleaned_data['age']
          qn = fm.cleaned_data['quantity']
          gn = fm.cleaned_data['gender']
          bg = fm.cleaned_data['blood_group']
          reg = Donor(name = nm, email = em, phone=ph , address = ad, age = ag,quantity = qn,gender= gn, blood_group = bg)
          reg.save()
          fm = Donorform()
    else:
        fm = Donorform()
    dnr = Donor.objects.all()
    return render(request,"donor.html",{'form':fm, 'dnr':dnr })

#this function will update donor data
@login_required(login_url="login")
def update_dnr(request , id):
    if request.method == 'POST':
        pi = Donor.objects.get(pk = id)
        fm = Donorform(request.POST , instance= pi)
        if fm.is_valid():
            fm.save()
    else:
        pi = Donor.objects.get(pk = id)
        fm = Donorform(instance=pi)
    return render(request,'update_dnr.html',{'form':fm})

#this funtion will delete donor data 
@login_required(login_url="login")
def delete_dnr(request,id):
    if request.method == 'POST':
        pi =Donor.objects.get(pk=id)
        pi.delete()
        return redirect('/donor')

#this function will add and show blood request data
def bloodreq(request):
    if request.method == 'POST':
        fom = Bloodreqform(request.POST)
        if fom.is_valid():
          nm =  fom.cleaned_data['name']
          em =  fom.cleaned_data['email']
          ph = fom.cleaned_data['phone']
          ad = fom.cleaned_data['address']
          ag = fom.cleaned_data['age']
          qn = fom.cleaned_data['quantity']
          gn = fom.cleaned_data['gender']
          bg = fom.cleaned_data['blood_group']
          regs = Bloodreq(name = nm, email = em, phone=ph , address = ad, age = ag,quantity = qn,gender= gn, blood_group = bg)
          regs.save()
          fom = Bloodreqform()
    else:
        fom = Bloodreqform()
    breq = Bloodreq.objects.all()
    return render(request,"bloodreq.html",{'form':fom , 'breq': breq})

#this function will update blood request data
@login_required(login_url="login")
def update_breq(request , id):
    if request.method == 'POST':
        qi = Bloodreq.objects.get(pk = id)
        fom = Bloodreqform(request.POST , instance= qi)
        if fom.is_valid():
            fom.save()
    else:
        qi = Bloodreq.objects.get(pk = id)
        fom = Bloodreqform(instance=qi)
    return render(request,'update_breq.html',{'form':fom})

#this funtion will delete blood request data 
@login_required(login_url="login")
def delete_breq(request,id):
    if request.method == 'POST':
        qi =Bloodreq.objects.get(pk=id)
        qi.delete()
        return redirect('/bloodreq')

#this function will add and show blood stock
@login_required(login_url="login")
def stock(request):
    if request.method == 'POST':
        fr = Stockform(request.POST)
        if fr.is_valid():
          nm =  fr.cleaned_data['name']
          em =  fr.cleaned_data['email']
          ph = fr.cleaned_data['phone']
          ad = fr.cleaned_data['address']
          qn = fr.cleaned_data['quantity']
          gn = fr.cleaned_data['gender']
          bg = fr.cleaned_data['blood_group']
          regis = Stock(name = nm, email = em, phone=ph , address = ad,quantity = qn,gender= gn, blood_group = bg)
          regis.save()
          fr = Stockform()
    else:
        fr = Stockform()
    stk = Stock.objects.all()
    return render(request,"stock.html", {'form':fr , 'stk':stk})

#this function will update blood stock data
@login_required(login_url="login")
def update_stk(request , id):
    if request.method == 'POST':
        ri = Stock.objects.get(pk = id)
        fr = Stockform(request.POST , instance= ri)
        if fr.is_valid():
            fr.save()
    else:
        ri = Stock.objects.get(pk = id)
        fr = Stockform(instance=ri)
    return render(request,'update_stk.html',{'form':fr})

#this funtion will delete  blood stockdata 
@login_required(login_url="login")
def delete_stk(request,id):
    if request.method == 'POST':
        ri =Stock.objects.get(pk=id)
        ri.delete()
        return redirect('/stock')

#this function will add contact data
def contact(request):
    if request.method == 'POST':
        fc = Contactform(request.POST)
        if fc.is_valid():
          nm =  fc.cleaned_data['name']
          em =  fc.cleaned_data['email']
          sb = fc.cleaned_data['subject']
          ms = fc.cleaned_data['message']
          regist = Contact(name = nm, email = em, subject=sb, message = ms)
          regist.save()
          fc = Contactform()
    else:
        fc = Contactform()
    ctc = Contact.objects.all()
    return render(request,"contact.html", {'form':fc , 'ctc':ctc})

def terms(request):
    return render(request,"terms.html")

def eligible(request):
    return render(request,"eligible.html")

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else: 
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                dj_login(request, user) 
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'login.html', context)

def logout(request):
   dj_logout(request)
   return redirect('login')

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
        context = { 'form':form}
    return render(request, 'register.html', context)
