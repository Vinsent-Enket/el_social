import stripe

from config import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(product_name):
    stripe_product = stripe.Product.create(
        name=product_name)  # судя по документации можно сразу указать параметры для прайса, но у меня не вышло
    return stripe_product['id']


def create_stripe_price(product_id, price):
    stripe_price = stripe.Price.create(currency="rub",
                                       unit_amount=price * 100,
                                       product=product_id
                                       )
    return stripe_price['id']


def get_payment_link(price_id):
    stripe_session = stripe.checkout.Session.create(
        success_url="https://example.com/success",
        line_items=[{"price": price_id, "quantity": 1}], mode="payment", )
    return stripe_session


def get_session_status(stripe_session_id):
    status = stripe.checkout.Session.retrieve(stripe_session_id)
    return status['payment_status']

# test_product = stripe.Product.create(name='Test_product')
#
# test_price = stripe.Price.create(currency="rub",
#                                  unit_amount=333 * 100,
#                                  product=test_product['id']
#                                  )
#
# test_session = stripe.checkout.Session.create(
#     success_url="https://example.com/success",
#     line_items=[{"price": test_price['id'],  "quantity": 1}], mode="payment",)
#
#
