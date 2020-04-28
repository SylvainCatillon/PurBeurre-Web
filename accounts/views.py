from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import CustomUserCreationForm


def create(request):
    """
    If the request method is GET, display a form to create a user.
    If the request method is POST:
    -test if the form is valid
    -use form.save() to create a new user
    -log the user in
    -redirect the user to "my account"

    Template: "accounts/create.html"
    Context: {"form": new CustomUserCreationForm}
    """
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("accounts:my_account")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/create.html", {"form": form})

def my_account(request):
    """
    If the user is authenticated, displays "my account" page.
    Else, redirects to the login page.

    Template: "accounts/my_account.html"
    """
    if request.user.is_authenticated:
        return render(request, "accounts/my_account.html")
    return redirect("accounts:login")
