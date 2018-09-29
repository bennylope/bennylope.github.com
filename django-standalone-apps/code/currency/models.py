"""
Example code from Django Standalone Apps

Author: Ben Lopatin
License: GPL(v3)
"""

from django.db import models


class Currency(models.Model):
    """
    >>> dollar = Currency(name="US Dollar", symbol="$", code="USD")
    """
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=5)
    code = models.CharField(max_length=5)
    formatting = models.CharField(max_length=100, default="{symbol}{amount}")

    def __str__(self):
        return self.name

    def format(self, amount):
        return self.formatting(symbol=self.symbol, amount=amount)
