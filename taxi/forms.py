from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from taxi.models import Driver, Car


class DriverCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            "first_name", "last_name", "license_number",)

    def clean_license_number(self):
        return validator_license(self.cleaned_data["license_number"])


class DriverLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ("license_number",)

    def clean_license_number(self):
        return validator_license(self.cleaned_data["license_number"])


def validator_license(license_number):
    if len(license_number) != 8:
        raise ValidationError("Length must be 8 characters!")
    if not license_number[:3].isupper() or not license_number[:3].isalpha():
        raise ValidationError("First 3 characters must be uppercase letters!")
    if not license_number[3:].isnumeric():
        raise ValidationError("Last 5 characters must be digits!")
    return license_number


class CarForm(forms.ModelForm):
    drivers = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Car
        fields = "__all__"