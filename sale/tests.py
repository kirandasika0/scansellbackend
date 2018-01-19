import time
from random import randint
from hashlib import sha256

from django.test import TestCase

from .models import Sale
from search.models import Book

class SaleModelTests(TestCase):
    test_sales = list()
    test_book = Book.objects.create(full_title="fd", link="http://google.com", uniform_title="")
    def setUp(self):
        for _ in xrange(100):
            new_sale = Sale()
            new_sale.seller_id = randint(1,100)
            new_sale.seller_username = sha256(str(time.time() + randint(1, 10000))).hexdigest()
            new_sale.book = self.test_book
            new_sale.price = randint(1, 1000)
            new_sale.save()
            self.test_sales.append(new_sale)

    def test_db_save(self):
       db_sales = Sale.objects.all().order_by("created_at")
       for test_sale, db_sale in zip(self.test_sales, db_sales):
           self.assertEqual(test_sale.seller_id, int(db_sale.seller_id))
           self.assertEqual(test_sale.seller_username, db_sale.seller_username)
           self.assertEqual(test_sale.price, int(db_sale.price))
        
