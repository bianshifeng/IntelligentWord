from django import forms

class RegistForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(
        label="password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )
    password2 = forms.CharField(
        label="password2",
        strip=False,
        widget=forms.PasswordInput(attrs={'autofocus': ''}),
    )
    email = forms.CharField(
        label="email",
        strip=False,
        widget=forms.EmailInput(attrs={'autofocus': ''}),
    )

    # def is_valid(self):
