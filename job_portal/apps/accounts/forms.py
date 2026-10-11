from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(
        choices=[(User.Role.SEEKER, "Job Seeker"), (User.Role.EMPLOYER, "Employer")],
        widget=forms.RadioSelect,
        initial=User.Role.SEEKER,
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != "role":
                field.widget.attrs.update({"class": "input"})
            field.widget.attrs.setdefault("placeholder", field.label or name.replace("_", " ").title())

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.role = self.cleaned_data["role"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "input", "placeholder": "Username or email"})
        self.fields["password"].widget.attrs.update({"class": "input", "placeholder": "••••••••"})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "location", "bio", "resume", "avatar")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "input"}),
            "last_name": forms.TextInput(attrs={"class": "input"}),
            "email": forms.EmailInput(attrs={"class": "input"}),
            "phone": forms.TextInput(attrs={"class": "input"}),
            "location": forms.TextInput(attrs={"class": "input"}),
            "bio": forms.Textarea(attrs={"class": "textarea", "rows": 3}),
            "resume": forms.ClearableFileInput(attrs={"class": "input"}),
            "avatar": forms.ClearableFileInput(attrs={"class": "input"}),
        }
