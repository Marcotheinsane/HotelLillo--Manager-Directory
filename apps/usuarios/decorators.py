from django.shortcuts import redirect
from django.contrib import messages

def solo_no_demo(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.username == "demo":
            messages.error(request, "La cuenta DEMO no puede realizar esta acción.")
            return redirect("home")
        return func(request, *args, **kwargs)
    return wrapper
