import json
from requests import get, post

UPC_SEARCH_URL = "http://www.searchupc.com/handlers/upcsearch.ashx?request_type=3&access_token=C4A45497-B6D0-4238-BEBF-4133CEDB4C21&upc="
GOOGLE_SEARCH_URL = "https://www.googleapis.com/books/v1/volumes?q="

def search_book(isbn):
    pass


def searchUPCStore(isbn):
    """
    This methods sends a request to the UPC store and check if the product is None
    and retuns response accordingly
    
    :return: dict
    """
    requestUrl = UPC_SEARCH_URL + isbn
    r = get(requestUrl)
    response = json.loads(r.content)
    if response is None:
        return None
    if response["0"]["productname"] == "N/A":
        return None
    
    responseDict = {
        'type': 'UPC',
        'product_name': response["0"]["productname"],
        'isbn': isbn
    }
    return responseDict

def searchGoogleBook(isbn):
    """
    This method searches for a isbn in google books and then parses the response
    and returns accordingly
    
    :return: dict
    
    """
    requestUrl = GOOGLE_SEARCH_URL + isbn + "+isbn"
    r = get(requestUrl)
    response = json.loads(r.content)
    responseDict = {
        'type': 'GOOGLE'
    }
    items = []
    for item in response["items"]:
        book = {
            'product_name': item["volumeInfo"]["title"],
            'publisher': item["publisher"],
            'isbn': item["industryIdentifiers"][1]["identifier"]
        }
        if item["imageLinks"]:
            book['image'] = item["imageLinks"]["thumbnail"]
        
        items.append(book)
    responseDict['items'] = items
    return responseDict


def cachedBook(isbnNumber, memcache):
    """
    Check if the book is already cached in memcache
    """
    cachedBooks = None
    if memcache.get_val("cached_books") == False:
        cachedBooks = {}
    else:
        cachedBooks = memcache.get_val("cached_books")
    
    if isbnNumber in cachedBooks.keys():
        return cachedBooks[isbnNumber]
    
    return cachedBooks

def cacheBook(isbnNumber, memcache, data=None):
    bookData = {
            'isbn_number': isbnNumber
            }
    bookData['data'] = data

    return memcache.set_key_value(isbnNumber, bookData)

