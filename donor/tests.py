from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
import json
from django.core import mail
from .models import Bloodreq, Contact, Donor, Payment, Stock
from django.test import override_settings


class PublicPageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_about_page_loads(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_submission_creates_record(self):
        response = self.client.post(
            reverse("contact"),
            {
                "name": "Asha",
                "email": "asha@example.com",
                "subject": "Donation",
                "message": "Need more details",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 1)
        self.assertEqual(Contact.objects.get().name, "Asha")

    def test_donor_submission_creates_record(self):
        response = self.client.post(
            reverse("donor"),
            {
                "name": "Ram",
                "email": "ram@example.com",
                "phone": 9800000000,
                "address": "Kathmandu",
                "age": 24,
                "quantity": 1,
                "gender": "Male",
                "blood_group": "O Positive",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Donor.objects.count(), 1)
        self.assertEqual(Donor.objects.get().blood_group, "O Positive")

    def test_blood_request_submission_creates_record(self):
        response = self.client.post(
            reverse("bloodreq"),
            {
                "name": "Sita",
                "email": "sita@example.com",
                "phone": 9800000001,
                "address": "Pokhara",
                "age": 30,
                "quantity": 2,
                "gender": "Female",
                "blood_group": "A Positive",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bloodreq.objects.count(), 1)
        self.assertEqual(Bloodreq.objects.get().quantity, 2)

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="noreply@bldonors.com",
        NOTIFICATION_EMAIL="admin@bldonors.com",
    )
    def test_blood_request_submission_sends_notifications(self):
        self.client.post(
            reverse("bloodreq"),
            {
                "name": "Sita",
                "email": "sita@example.com",
                "phone": 9800000001,
                "address": "Pokhara",
                "age": 30,
                "quantity": 2,
                "gender": "Female",
                "blood_group": "A Positive",
            },
        )

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].subject, "New Blood Request Submitted")
        self.assertEqual(mail.outbox[1].to, ["sita@example.com"])

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="noreply@bldonors.com",
    )
    def test_payment_submission_creates_record_and_sends_email(self):
        response = self.client.post(
            reverse("payment"),
            {
                "donor_name": "Payment User",
                "email": "pay@example.com",
                "phone": "9800000099",
                "amount": "1500.00",
                "purpose": "Donation",
                "payment_method": "eSewa",
                "remarks": "Semester project support",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.get().status, "Completed")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Payment Received")


class AuthProtectedViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="secret123")
        self.stock = Stock.objects.create(
            name="Blood Bank",
            email="bank@example.com",
            phone=9800000002,
            address="Lalitpur",
            quantity=5,
            gender="Other",
            blood_group="AB Positive",
        )
        self.donor = Donor.objects.create(
            name="Hari",
            email="hari@example.com",
            phone=9800000003,
            address="Bhaktapur",
            age=28,
            quantity=1,
            gender="Male",
            blood_group="B Positive",
        )

    def test_stock_page_requires_login(self):
        response = self.client.get(reverse("stock"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_logged_in_user_can_open_stock_page(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("stock"))
        self.assertEqual(response.status_code, 200)

    def test_reports_page_requires_login(self):
        response = self.client.get(reverse("reports"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_logged_in_user_can_open_reports_page(self):
        Bloodreq.objects.create(
            name="Req User",
            email="req@example.com",
            phone=9800000004,
            address="Kathmandu",
            age=31,
            quantity=2,
            gender="Female",
            blood_group="AB Positive",
        )
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("reports"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reports Dashboard")
        self.assertContains(response, "Total Donors")

    def test_logged_in_user_can_export_report_csv(self):
        Payment.objects.create(
            donor_name="Supporter",
            email="support@example.com",
            phone="9800000015",
            amount="2000.00",
            purpose="Campaign",
            payment_method="Cash",
            status="Completed",
            transaction_id="BLD-TEST0001",
        )
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("export_reports_csv"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("Total Donors", response.content.decode("utf-8"))
        self.assertIn("Total Amount Received", response.content.decode("utf-8"))

    def test_live_report_data_requires_login(self):
        response = self.client.get(reverse("live_report_data"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)

    def test_logged_in_user_can_get_live_report_data(self):
        Payment.objects.create(
            donor_name="Supporter",
            email="support@example.com",
            phone="9800000016",
            amount="2500.00",
            purpose="Donation",
            payment_method="Khalti",
            status="Completed",
            transaction_id="BLD-TEST0002",
        )
        self.client.login(username="tester", password="secret123")
        response = self.client.get(reverse("live_report_data"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIn("total_units", response.json()["data"])
        self.assertIn("payment_total", response.json()["data"])
        self.assertEqual(response.json()["data"]["payment_total"], 1)

    def test_logged_in_user_can_update_donor(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.post(
            reverse("updatednr", args=[self.donor.id]),
            {
                "name": "Hari Updated",
                "email": "hari@example.com",
                "phone": 9800000003,
                "address": "Bhaktapur",
                "age": 29,
                "quantity": 2,
                "gender": "Male",
                "blood_group": "B Positive",
            },
        )

        self.assertRedirects(response, reverse("donor"))
        self.donor.refresh_from_db()
        self.assertEqual(self.donor.name, "Hari Updated")
        self.assertEqual(self.donor.quantity, 2)

    def test_logged_in_user_can_delete_stock(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.post(reverse("deletestk", args=[self.stock.id]))

        self.assertRedirects(response, reverse("stock"))
        self.assertFalse(Stock.objects.filter(id=self.stock.id).exists())

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
        DEFAULT_FROM_EMAIL="noreply@bldonors.com",
        NOTIFICATION_EMAIL="admin@bldonors.com",
        LOW_STOCK_ALERT_LEVEL=5,
    )
    def test_low_stock_update_sends_email_alert(self):
        self.client.login(username="tester", password="secret123")
        response = self.client.post(
            reverse("updatestk", args=[self.stock.id]),
            {
                "name": "Blood Bank",
                "email": "bank@example.com",
                "phone": 9800000002,
                "address": "Lalitpur",
                "quantity": 3,
                "gender": "Other",
                "blood_group": "AB Positive",
            },
        )

        self.assertRedirects(response, reverse("stock"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Low Blood Stock Alert")


class AuthFlowTests(TestCase):
    def test_register_creates_user(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "newuser",
                "email": "newuser@example.com",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_redirects_authenticated_user_home(self):
        User.objects.create_user(username="member", password="secret123")
        self.client.login(username="member", password="secret123")

        response = self.client.get(reverse("login"))

        self.assertRedirects(response, reverse("home"))


class ApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="apiuser", password="secret123")
        self.donor = Donor.objects.create(
            name="Api Donor",
            email="donor@example.com",
            phone=9800000010,
            address="Kathmandu",
            age=25,
            quantity=1,
            gender="Male",
            blood_group="O Positive",
        )
        self.stock = Stock.objects.create(
            name="Main Bank",
            email="stock@example.com",
            phone=9800000011,
            address="Lalitpur",
            quantity=4,
            gender="Female",
            blood_group="A Positive",
        )

    def test_api_summary_returns_counts(self):
        response = self.client.get(reverse("api-summary"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")
        self.assertIn("donor_total", response.json()["data"])

    def test_api_donors_list_returns_json(self):
        response = self.client.get(reverse("api-donors"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["data"]), 1)

    def test_api_donor_create_works(self):
        response = self.client.post(
            reverse("api-donors"),
            data=json.dumps(
                {
                    "name": "Json Donor",
                    "email": "json@example.com",
                    "phone": 9800000012,
                    "address": "Pokhara",
                    "age": 22,
                    "quantity": 1,
                    "gender": "Female",
                    "blood_group": "B Positive",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Donor.objects.count(), 2)

    def test_api_stock_create_requires_login(self):
        response = self.client.post(
            reverse("api-stocks"),
            data=json.dumps(
                {
                    "name": "Json Stock",
                    "email": "stock2@example.com",
                    "phone": 9800000013,
                    "address": "Bhaktapur",
                    "quantity": 6,
                    "gender": "Other",
                    "blood_group": "AB Positive",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)

    def test_api_login_and_session_work(self):
        login_response = self.client.post(
            reverse("api-login"),
            data=json.dumps({"username": "apiuser", "password": "secret123"}),
            content_type="application/json",
        )
        session_response = self.client.get(reverse("api-session"))

        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(session_response.json()["data"]["is_authenticated"])

    def test_api_delete_donor_requires_login(self):
        response = self.client.delete(reverse("api-donor-detail", args=[self.donor.id]))
        self.assertEqual(response.status_code, 403)

    def test_api_delete_donor_after_login(self):
        self.client.login(username="apiuser", password="secret123")
        response = self.client.delete(reverse("api-donor-detail", args=[self.donor.id]))

        self.assertEqual(response.status_code, 200)
        self.assertFalse(Donor.objects.filter(id=self.donor.id).exists())
