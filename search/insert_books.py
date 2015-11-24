import json, os
from models import Product


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.loads(open(BASE_DIR + '/search/book.json').read())


def start():
    for book in data["book"]:
        try:
            Product.objects.create(full_title=book["full_title"], link=book["link"], 
                                uniform_title=book["uniform_title"])
        except:
            print "Error in inserting"
        print book["uniform_title"]