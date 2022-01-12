from random import randint

from app_orders.models import Orders
from loguru import logger


def order_payment(order_pk: int, card_number: str) -> dict:
    """
    :order_pk: номер заказа
    :card_number: номер карты покупателя
    Функция производит запрос в сервис оплаты,
    если ответ True, обновляет статус заказа и счет
    клиента. После этого возвращается ответ от сервиса
    оплаты с сообщением.
    :return: dict(status: bool, message: str)
    """
    response = get_order_payment_status(card_number)
    if response["status"]:
        order = Orders.objects.get(pk=order_pk)
        order.payment_state = True
        order.bank_account = card_number
        order.save()
    return response


def get_order_payment_status(card_number: str) -> dict:
    """Функция - замена настоящего сервиса оплаты,
    если номер карты четный возвращается ответ об успешной оплате
    в ином случае возвращается ответ о неудаче и одна из трех ошибок.
    :card_number: номер карты покупателя.
    :return: dict(status: bool, message: str).
    """
    if int(card_number[-1]) != 0 and (int(card_number) % 2) == 0:
        response = {"status": True, "message": "Success!"}
        return response
    else:
        dice = randint(1, 3)
        response = {}
        if dice == 3:
            response["message"] = "Server is unreachable, please try later."
            logger.debug("Server is unreachable, please try later.")
        elif dice == 2:
            logger.debug("Your payment account in black list!")
            response["message"] = "Your payment account in black list!"
        else:
            logger.debug("Wrong payment")
            response["message"] = "Wrong payment"
        response["status"] = False
        return response
