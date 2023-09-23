from django.shortcuts import redirect


def home_handler(request):
    return redirect("home")
