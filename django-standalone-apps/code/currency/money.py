from decimal import Decimal


class Money(Decimal):
    """
    """
    def __new__(cls, *args, **kwargs):
        cls.currency = kwargs.pop('currency', None)
        super(Money, cls).__new__(cls, *args, **kwargs)

