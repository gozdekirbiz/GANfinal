from django import forms


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class DeleteAccountForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)


class SuggestionsForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
