from django.conf import settings
from django.core.mail import send_mail


def get_notification_recipient():
    return getattr(settings, "NOTIFICATION_EMAIL", "admin@bldonors.com")


def send_request_notification(blood_request):
    subject = "New Blood Request Submitted"
    message = (
        "A new blood request has been submitted.\n\n"
        f"Name: {blood_request.name}\n"
        f"Blood Group: {blood_request.blood_group}\n"
        f"Quantity: {blood_request.quantity}\n"
        f"Phone: {blood_request.phone}\n"
        f"Address: {blood_request.address}\n"
    )
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [get_notification_recipient()],
        fail_silently=True,
    )


def send_request_received_email(blood_request):
    subject = "Blood Request Received"
    message = (
        f"Hello {blood_request.name},\n\n"
        "Your blood request has been received by the Bldonors system.\n"
        f"Requested blood group: {blood_request.blood_group}\n"
        f"Requested quantity: {blood_request.quantity}\n\n"
        "We will contact you if matching stock or donor information becomes available."
    )
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [blood_request.email],
        fail_silently=True,
    )


def send_low_stock_notification(stock):
    threshold = getattr(settings, "LOW_STOCK_ALERT_LEVEL", 5)
    if stock.quantity > threshold:
        return 0

    subject = "Low Blood Stock Alert"
    message = (
        "Blood stock is low.\n\n"
        f"Blood Group: {stock.blood_group}\n"
        f"Units Available: {stock.quantity}\n"
        f"Updated By: {stock.name}\n"
        f"Contact Email: {stock.email}\n"
    )
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [get_notification_recipient()],
        fail_silently=True,
    )


def send_payment_received_email(payment):
    subject = "Payment Received"
    message = (
        f"Hello {payment.donor_name},\n\n"
        "Thank you for your support.\n"
        f"Transaction ID: {payment.transaction_id}\n"
        f"Amount: Rs. {payment.amount}\n"
        f"Purpose: {payment.purpose}\n"
        f"Payment Method: {payment.payment_method}\n"
        f"Status: {payment.status}\n"
    )
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [payment.email],
        fail_silently=True,
    )
