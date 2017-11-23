""" All global utilities for Quicksell server """
import json
from django.http import HttpResponse

CONTENT_TYPE = "application/json"

class ServeResponse(object):
    """ Generic response for Quicksell API. """
    def __init__(self):
        pass
    
    @staticmethod
    def serve_response(data, status_code, *args, **kwargs):
        """ serve_response is for serving a successful response. """
        if data is None or status_code is None:
            raise ValueError("Provide data and status code.")
        
        if type(data) is str or type(data) is unicode:
            try:
                if kwargs["is_proto"]:
                    return HttpResponse(data, status=status_code)
            except KeyError:
                pass
                
            return HttpResponse(data, content_type=CONTENT_TYPE,
                                status=status_code)

        return HttpResponse(json.dumps(data), content_type=CONTENT_TYPE,
                            status=status_code)
    
    @staticmethod
    def serve_error(error, status_code):
        """ serve_error is for serving a error response. """
        if error is None or status_code is None:
            raise ValueError("Provide data and status code.")

        return HttpResponse(json.dumps({"status":status_code, "error": error}),
                            content_type=CONTENT_TYPE, status=status_code)
