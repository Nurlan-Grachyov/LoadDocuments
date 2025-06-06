import stripe
from django.http import JsonResponse

from config.settings import API_KEY

stripe.api_key = API_KEY


def create_price(amount):
    """
    Create a price for an object
    """

    price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "tuition fees"},
    )
    return price


def create_session(price):
    """
    Create payment session
    """

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")


def test_session(request, session_id):
    """
    The viewing a payment session with session ID
    """

    session = stripe.checkout.Session.retrieve(session_id)
    return JsonResponse({"session": session})
