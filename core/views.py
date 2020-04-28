from django.shortcuts import render

def index(request):
    """
    Display the home page

    Template: "core/index.html"
    """
    return render(request, "core/index.html")

def legal(request):
    """
    Display the legal terms

    Template: "core/legal.html"
    """
    return render(request, "core/legal.html")
