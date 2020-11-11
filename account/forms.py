# forms allows forms to be created
from django import forms

# check_password compares the password entered to the encrypted password stored
from django.contrib.auth.hashers import check_password

# Allows database to be accessed and updated by forms
from . import models

# Form that provides the user with username and password fields
class LogInForm(forms.Form):
    username = forms.EmailField(label = "Email")
    password = forms.CharField(widget = forms.PasswordInput)

# Form that provides the user with first name, last name, email, username and password fields
class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(label = "Password", widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Confirm Password", widget = forms.PasswordInput)

    # Fields taken from User table are first_name, last_name and email
    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]

    # It is ensured the passwords match, otherwise an error is raised
    def clean_password2(self):
        # Two passwords are taken in string form
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # If the two passwords don't match
        if password1 != password2:
            raise forms.ValidationError("The passwords you have entered do not match.")
        return password2

    # If no errors are raised, this function is run
    def save(self):
        # User record correcsponding to user that made the request
        user = super(SignUpForm, self).save(commit = False)
        # Users password is set to encrypted version of password entered into form
        user.set_password(self.cleaned_data["password1"])
        user.save()

# Form that provides user with old password, new password and new password confirm fields
class ChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(label = "Old Password", widget = forms.PasswordInput)
    password1 = forms.CharField(label = "New Password", widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Confirm New Password", widget = forms.PasswordInput)

    # User that the password being changed to is entered as parameter
    def __init__(self, user, data = None):
        self.user = user
        super(ChangePasswordForm, self).__init__(data = data)

    # It is ensured the following things are valid
    def clean(self):
        data = self.cleaned_data

        # Empty dictionary for errors to be added to
        errors = {}

        # If the two new passwords do not match an error is made
        if data.get("password1") != data.get("password2"):
            errors.update({"password1": "The passwords you have entered do not match."})

        # If the old password is not the user's password an error is raised
        if self.user.check_password(data.get("oldPassword")) == False:
            errors.update({"oldPassword": "The password you have entered is incorrect."})

        # If errors do exist
        if errors != {}:
            raise forms.ValidationError(errors)

        return data
