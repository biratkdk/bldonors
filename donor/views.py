import csv
import uuid

from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import Bloodreqform, Contactform, Donorform, Paymentform, Stockform, createuserform
from .models import Bloodreq, Contact, Donor, Payment, Stock
from .notifications import (
    send_low_stock_notification,
    send_payment_received_email,
    send_request_notification,
    send_request_received_email,
)

def home(request):
    return render(request, "base.html")

def blog(request):
    return render(request, "blog.html")

def about(request):
    return render(request, "about.html")

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

@login_required(login_url="login")
def update_dnr(request , id):
    pi = get_object_or_404(Donor, pk=id)
    if request.method == 'POST':
        fm = Donorform(request.POST , instance= pi)
        if fm.is_valid():
            fm.save()
            return redirect("donor")
    else:
        fm = Donorform(instance=pi)
    return render(request,'update_dnr.html',{'form':fm})

@login_required(login_url="login")
def delete_dnr(request,id):
    if request.method == 'POST':
        pi = get_object_or_404(Donor, pk=id)
        pi.delete()
        return redirect('donor')
    return redirect('donor')

def bloodreq(request):
    if request.method == 'POST':
        fom = Bloodreqform(request.POST)
        if fom.is_valid():
          regs = fom.save()
          send_request_notification(regs)
          send_request_received_email(regs)
          messages.success(request, "Blood request submitted successfully.")
          fom = Bloodreqform()
    else:
        fom = Bloodreqform()
    breq = Bloodreq.objects.all()
    return render(request,"bloodreq.html",{'form':fom , 'breq': breq})

@login_required(login_url="login")
def update_breq(request , id):
    qi = get_object_or_404(Bloodreq, pk=id)
    if request.method == 'POST':
        fom = Bloodreqform(request.POST , instance= qi)
        if fom.is_valid():
            fom.save()
            return redirect("bloodreq")
    else:
        fom = Bloodreqform(instance=qi)
    return render(request,'update_breq.html',{'form':fom})

@login_required(login_url="login")
def delete_breq(request,id):
    if request.method == 'POST':
        qi = get_object_or_404(Bloodreq, pk=id)
        qi.delete()
        return redirect('bloodreq')
    return redirect('bloodreq')

@login_required(login_url="login")
def stock(request):
    if request.method == 'POST':
        fr = Stockform(request.POST)
        if fr.is_valid():
          regis = fr.save()
          send_low_stock_notification(regis)
          messages.success(request, "Blood stock saved successfully.")
          fr = Stockform()
    else:
        fr = Stockform()
    stk = Stock.objects.all()
    return render(request,"stock.html", {'form':fr , 'stk':stk})

@login_required(login_url="login")
def update_stk(request , id):
    ri = get_object_or_404(Stock, pk=id)
    if request.method == 'POST':
        fr = Stockform(request.POST , instance= ri)
        if fr.is_valid():
            stock_obj = fr.save()
            send_low_stock_notification(stock_obj)
            return redirect("stock")
    else:
        fr = Stockform(instance=ri)
    return render(request,'update_stk.html',{'form':fr})

@login_required(login_url="login")
def delete_stk(request,id):
    if request.method == 'POST':
        ri = get_object_or_404(Stock, pk=id)
        ri.delete()
        return redirect('stock')
    return redirect('stock')

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


def payment(request):
    if request.method == "POST":
        form = Paymentform(request.POST)
        if form.is_valid():
            payment_obj = form.save(commit=False)
            payment_obj.transaction_id = "BLD-" + uuid.uuid4().hex[:10].upper()
            payment_obj.status = "Completed"
            payment_obj.save()
            send_payment_received_email(payment_obj)
            messages.success(request, "Payment record saved successfully.")
            form = Paymentform()
    else:
        form = Paymentform()

    recent_payments = Payment.objects.all().order_by("-created_at")[:10]
    return render(request, "payment.html", {"form": form, "recent_payments": recent_payments})

def build_report_snapshot():
    donor_total = Donor.objects.count()
    request_total = Bloodreq.objects.count()
    stock_total = Stock.objects.count()
    contact_total = Contact.objects.count()
    payment_total = Payment.objects.count()
    total_units = Stock.objects.aggregate(total=Sum("quantity"))["total"] or 0
    total_amount_received = Payment.objects.filter(status="Completed").aggregate(total=Sum("amount"))["total"] or 0
    donor_by_group = list(
        Donor.objects.values("blood_group").annotate(total=Count("id")).order_by("blood_group")
    )
    request_by_group = list(
        Bloodreq.objects.values("blood_group").annotate(total=Count("id")).order_by("blood_group")
    )
    stock_by_group = list(
        Stock.objects.values("blood_group").annotate(total_units=Sum("quantity")).order_by("blood_group")
    )
    low_stock_items = list(
        Stock.objects.filter(quantity__lte=5)
        .order_by("quantity", "blood_group")
        .values("name", "blood_group", "quantity")
    )

    return {
        "donor_total": donor_total,
        "request_total": request_total,
        "stock_total": stock_total,
        "contact_total": contact_total,
        "payment_total": payment_total,
        "total_units": total_units,
        "total_amount_received": total_amount_received,
        "donor_by_group": donor_by_group,
        "request_by_group": request_by_group,
        "stock_by_group": stock_by_group,
        "low_stock_items": low_stock_items,
    }

@login_required(login_url="login")
def reports(request):
    context = build_report_snapshot()
    return render(request, "reports.html", context)

@login_required(login_url="login")
def live_report_data(request):
    return JsonResponse({"status": "success", "data": build_report_snapshot()})

@login_required(login_url="login")
def export_reports_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="bldonors_report.csv"'

    writer = csv.writer(response)
    writer.writerow(["Section", "Label", "Value"])
    writer.writerow(["Summary", "Total Donors", Donor.objects.count()])
    writer.writerow(["Summary", "Total Blood Requests", Bloodreq.objects.count()])
    writer.writerow(["Summary", "Total Stock Entries", Stock.objects.count()])
    writer.writerow(["Summary", "Total Contacts", Contact.objects.count()])
    writer.writerow(["Summary", "Total Payments", Payment.objects.count()])
    writer.writerow(["Summary", "Total Units Available", Stock.objects.aggregate(total=Sum("quantity"))["total"] or 0])
    writer.writerow(["Summary", "Total Amount Received", Payment.objects.filter(status="Completed").aggregate(total=Sum("amount"))["total"] or 0])
    writer.writerow([])

    writer.writerow(["Donors By Group", "Blood Group", "Count"])
    for item in Donor.objects.values("blood_group").annotate(total=Count("id")).order_by("blood_group"):
        writer.writerow(["Donors By Group", item["blood_group"], item["total"]])

    writer.writerow([])
    writer.writerow(["Requests By Group", "Blood Group", "Count"])
    for item in Bloodreq.objects.values("blood_group").annotate(total=Count("id")).order_by("blood_group"):
        writer.writerow(["Requests By Group", item["blood_group"], item["total"]])

    writer.writerow([])
    writer.writerow(["Stock By Group", "Blood Group", "Units"])
    for item in Stock.objects.values("blood_group").annotate(total_units=Sum("quantity")).order_by("blood_group"):
        writer.writerow(["Stock By Group", item["blood_group"], item["total_units"]])

    writer.writerow([])
    writer.writerow(["Payments", "Transaction ID", "Amount"])
    for item in Payment.objects.filter(status="Completed").order_by("-created_at")[:20]:
        writer.writerow(["Payments", item.transaction_id, item.amount])

    return response

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
