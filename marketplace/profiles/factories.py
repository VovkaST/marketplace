import datetime
from decimal import Decimal

import factory


class DeliveryMethodsFactory(factory.DictFactory):
    name = factory.Sequence(lambda n: f"Метод доставки {n}")
    price = factory.Sequence(lambda n: Decimal(1) * n)


class PaymentMethodsFactory(factory.DictFactory):
    name = factory.Sequence(lambda n: f"Способ оплаты {n}")


class OrdersFactory(factory.DictFactory):

    pk = factory.Sequence(lambda n: n)
    user = 1
    total_sum = factory.Sequence(lambda n: Decimal(100) * n)
    date_time = datetime.datetime.now()
    delivery = factory.SubFactory(DeliveryMethodsFactory)
    payment = factory.SubFactory(PaymentMethodsFactory)
    payment_state = False
    city = factory.Sequence(lambda n: f"Город {n}")
    address = factory.Sequence(lambda n: f"Адрес {n}")
    comment = factory.Sequence(lambda n: f"Комментарий {n}")
    deleted = False
