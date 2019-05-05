from functools import wraps

def auth(method):

    @wraps(method)
    def autFunc(self, request, *args, **kwargs):


        return method(request,kwargs["id"])