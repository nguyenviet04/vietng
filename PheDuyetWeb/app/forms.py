# credit_app/forms.py
from django import forms
from .models import CreditApplication
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)


class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        # Liệt kê tất cả 15 trường bạn muốn người dùng nhập
        fields = [
            'gender', 'age', 'debt', 'married', 'bank_customer', 'industry',
            'ethnicity', 'years_employed', 'prior_default', 'employed',
            'credit_score', 'drivers_license', 'citizen', 'zip_code', 'income'
        ]

        # Tùy chỉnh widgets để giao diện đẹp hơn (thêm placeholder)
        widgets = {
            'age': forms.NumberInput(attrs={'placeholder': 'VD: 34.5'}),
            'debt': forms.NumberInput(attrs={'placeholder': 'VD: 1.25'}),
            'years_employed': forms.NumberInput(attrs={'placeholder': 'VD: 3.5'}),
            'credit_score': forms.NumberInput(attrs={'placeholder': 'VD: 680'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'VD: 700000'}),
            'income': forms.NumberInput(attrs={'placeholder': 'VD: 560'}),
        }