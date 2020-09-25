import json

from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import Bloodreqform, Donorform, Stockform
from .models import Bloodreq, Donor, Stock


def donor_to_dict(donor):
    return {
        "id": donor.id,
        "name": donor.name,
        "email": donor.email,
        "phone": donor.phone,
        "address": donor.address,
        "age": donor.age,
        "quantity": donor.quantity,
        "gender": donor.gender,
        "blood_group": donor.blood_group,
    }


def bloodreq_to_dict(bloodreq):
    return {
        "id": bloodreq.id,
        "name": bloodreq.name,
        "email": bloodreq.email,
        "phone": bloodreq.phone,
        "address": bloodreq.address,
        "age": bloodreq.age,
        "quantity": bloodreq.quantity,
        "gender": bloodreq.gender,
        "blood_group": bloodreq.blood_group,
    }


def stock_to_dict(stock):
    return {
        "id": stock.id,
        "name": stock.name,
        "email": stock.email,
        "phone": stock.phone,
        "address": stock.address,
        "quantity": stock.quantity,
        "gender": stock.gender,
        "blood_group": stock.blood_group,
    }


def load_json_data(request):
    try:
        return json.loads(request.body.decode("utf-8") or "{}")
    except (TypeError, ValueError, UnicodeDecodeError):
        return None


def method_not_allowed():
    return JsonResponse({"status": "error", "message": "Method not allowed"}, status=405)


def login_required_json(request):
    if request.user.is_authenticated:
        return None
    return JsonResponse(
        {"status": "error", "message": "Login required for this action"},
        status=403,
    )


@require_http_methods(["GET"])
def api_summary(request):
    donor_total = Donor.objects.count()
    request_total = Bloodreq.objects.count()
    stock_total = Stock.objects.count()
    available_units = Stock.objects.aggregate(total=Sum("quantity"))["total"] or 0
    blood_groups = list(
        Stock.objects.values("blood_group").annotate(total=Sum("quantity")).order_by("blood_group")
    )

    return JsonResponse(
        {
            "status": "success",
            "data": {
                "donor_total": donor_total,
                "request_total": request_total,
                "stock_total": stock_total,
                "available_units": available_units,
                "blood_groups": blood_groups,
            },
        }
    )


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_donors(request):
    if request.method == "GET":
        donors = [donor_to_dict(donor) for donor in Donor.objects.all().order_by("-id")]
        return JsonResponse({"status": "success", "data": donors})

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Donorform(data)
    if form.is_valid():
        donor = form.save()
        return JsonResponse({"status": "success", "data": donor_to_dict(donor)}, status=201)
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_donor_detail(request, id):
    try:
        donor = Donor.objects.get(pk=id)
    except Donor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Donor not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"status": "success", "data": donor_to_dict(donor)})

    auth_error = login_required_json(request)
    if auth_error:
        return auth_error

    if request.method == "DELETE":
        donor.delete()
        return JsonResponse({"status": "success", "message": "Donor deleted"})

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Donorform(data, instance=donor)
    if form.is_valid():
        donor = form.save()
        return JsonResponse({"status": "success", "data": donor_to_dict(donor)})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_blood_requests(request):
    if request.method == "GET":
        requests = [
            bloodreq_to_dict(bloodreq) for bloodreq in Bloodreq.objects.all().order_by("-id")
        ]
        return JsonResponse({"status": "success", "data": requests})

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Bloodreqform(data)
    if form.is_valid():
        bloodreq = form.save()
        return JsonResponse(
            {"status": "success", "data": bloodreq_to_dict(bloodreq)},
            status=201,
        )
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_blood_request_detail(request, id):
    try:
        bloodreq = Bloodreq.objects.get(pk=id)
    except Bloodreq.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Blood request not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"status": "success", "data": bloodreq_to_dict(bloodreq)})

    auth_error = login_required_json(request)
    if auth_error:
        return auth_error

    if request.method == "DELETE":
        bloodreq.delete()
        return JsonResponse({"status": "success", "message": "Blood request deleted"})

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Bloodreqform(data, instance=bloodreq)
    if form.is_valid():
        bloodreq = form.save()
        return JsonResponse({"status": "success", "data": bloodreq_to_dict(bloodreq)})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def api_stocks(request):
    if request.method == "GET":
        stocks = [stock_to_dict(stock) for stock in Stock.objects.all().order_by("-id")]
        return JsonResponse({"status": "success", "data": stocks})

    auth_error = login_required_json(request)
    if auth_error:
        return auth_error

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Stockform(data)
    if form.is_valid():
        stock = form.save()
        return JsonResponse({"status": "success", "data": stock_to_dict(stock)}, status=201)
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def api_stock_detail(request, id):
    try:
        stock = Stock.objects.get(pk=id)
    except Stock.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Stock not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"status": "success", "data": stock_to_dict(stock)})

    auth_error = login_required_json(request)
    if auth_error:
        return auth_error

    if request.method == "DELETE":
        stock.delete()
        return JsonResponse({"status": "success", "message": "Stock deleted"})

    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    form = Stockform(data, instance=stock)
    if form.is_valid():
        stock = form.save()
        return JsonResponse({"status": "success", "data": stock_to_dict(stock)})
    return JsonResponse({"status": "error", "errors": form.errors}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def api_login(request):
    data = load_json_data(request)
    if data is None:
        return JsonResponse({"status": "error", "message": "Invalid JSON data"}, status=400)

    user = authenticate(
        request,
        username=data.get("username", ""),
        password=data.get("password", ""),
    )
    if user is None:
        return JsonResponse({"status": "error", "message": "Invalid username or password"}, status=400)

    dj_login(request, user)
    return JsonResponse(
        {
            "status": "success",
            "data": {"username": user.username, "is_authenticated": True},
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def api_logout(request):
    dj_logout(request)
    return JsonResponse({"status": "success", "message": "Logged out"})


@require_http_methods(["GET"])
def api_session(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "status": "success",
                "data": {"username": request.user.username, "is_authenticated": True},
            }
        )
    return JsonResponse(
        {
            "status": "success",
            "data": {"username": "", "is_authenticated": False},
        }
    )
