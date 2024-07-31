# decorators.py
from django.core.exceptions import PermissionDenied

def jefe_bienes_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.empleado.es_jefe_bienes:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
