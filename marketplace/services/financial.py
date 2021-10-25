import datetime
from random import randint

from loguru import logger


def order_payment(card_number: str) -> bool:
    if int(card_number[-1]) != 0 and (int(card_number) % 2) == 0:
        return True
    else:
        dice = randint(1, 3)
        if dice == 3:
            logger.debug("Server is unreachable, please try later.")
        elif dice == 2:
            logger.debug("Your payment account in black list!")
        else:
            logger.debug("Wrong payment")
        return False


def get_order_payment_status():
    if datetime.datetime.now().second > 30:
        return True
    else:
        return False
