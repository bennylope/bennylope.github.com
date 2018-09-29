"""
Example code from Django Standalone Apps

Author: Ben Lopatin
License: GPL(v3)
"""

from django.test import TestCase

from .models import Currency


class CurrencyFormattingTests(TestCase):

    def test_usd(self):
        dollar = Currency(name="US Dollar", symbol="$", code="USD")
        self.assertEqual("$100", dollar.format(100))

    def test_french_euro(self):
        euro = Currency(name="Euro", symbol="€", code="EUR", formatting="{amount} {symbol}")
        self.assertEqual("100 €", euro.format(100))
