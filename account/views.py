# render used to return HTML responses
# get_object_or_404 raises a 404 error if a record cannot be found
from django.shortcuts import render, get_object_or_404

# authenticate checks that a users email and password is correct
# login provides a user with a login cookie to keep user logged in
# login removes a users login cookie to log user out
from django.contrib.auth import authenticate, login, logout

# redirect redirects the user to a url path
from django.shortcuts import redirect

# Imports forms and database tables
from . import forms, models

# Provides HTML page with account details
def account(request):
    return render(request, "account/account.html")

# Provides log in form and logs user in
def logIn(request):
    # The log in form
    form = forms.LogInForm(request.POST or None)

    # The users input to the log in form is initially assumed to be valid
    valid = True

    # If the request is an HTML POST request the form has be submitted
    if request.method == "POST":
        # If there are no errors in the form
        if form.is_valid():

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            # Username and password are tested to see if they are correct
            user = authenticate(request, username = username, password = password)

            # If the username and passsword are correct
            if user is not None:
                # User is logged in
                login(request, user)
                # User redirected to homepage
                return redirect("/")

            # If the username and password are incorrect the log in form is marked as invalid
            else:
                valid = False

    # Returns the HTML page with the log in form
    return render(request, "account/logIn.html", {
        "logInForm": form,
        "valid": valid
    })

# Logs the user out and redirects them to homepage
def logOut(request):
    logout(request)
    return redirect("/")

# Provides the sign up form and signs a new user up
def signUp(request):
    # The sign up form
    form = forms.SignUpForm(request.POST or None)

    # If the request is an HTML POST request the form has been submitted
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")

            # New user is saved to database
            form.save()

            # Username and password are tested to see if they are correct
            user = authenticate(request, username = username, password = password)

            # If the usernamd and password are correct
            if user is not None:
                # User is logged in
                login(request, user)
                # User redirected to homepage
                return redirect("/")

    # Returns the HTML page with the sign up form
    return render(request, "account/signUp.html", {
        "signUpForm": form
    })

# Provides the change password form and changes the user's password
def changePassword(request):
    # The user who wants to change their password
    user = models.User.objects.get(pk = request.user.id)
    # The change password form
    form = forms.ChangePasswordForm(user = user, data = request.POST or None)

    # If the request is an HTML post request the form has been submitted
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            # The users password is set to the new encrypted password
            user.set_password(form.cleaned_data.get("password1"))
            user.save()

            # Username and password are tested to see if they are correct
            user = authenticate(request, username = user.email, password = form.cleaned_data.get("password1"))

            # If the username and password are correct
            if user is not None:
                # User is logged in
                login(request, user)
                # User is redirected to homepage
                return redirect("/")

    # Returns the HTML page with the change password form
    return render(request, "account/changePassword.html", {
        "changePasswordForm": form,
    })
