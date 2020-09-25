from django.urls import path

from . import api_views

urlpatterns = [
    path("summary/", api_views.api_summary, name="api-summary"),
    path("donors/", api_views.api_donors, name="api-donors"),
    path("donors/<int:id>/", api_views.api_donor_detail, name="api-donor-detail"),
    path("blood-requests/", api_views.api_blood_requests, name="api-blood-requests"),
    path(
        "blood-requests/<int:id>/",
        api_views.api_blood_request_detail,
        name="api-blood-request-detail",
    ),
    path("stocks/", api_views.api_stocks, name="api-stocks"),
    path("stocks/<int:id>/", api_views.api_stock_detail, name="api-stock-detail"),
    path("login/", api_views.api_login, name="api-login"),
    path("logout/", api_views.api_logout, name="api-logout"),
    path("session/", api_views.api_session, name="api-session"),
]
