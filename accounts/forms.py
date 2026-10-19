from django import forms
from django.contrib.auth import authenticate
from .models import User

class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور (8 أحرف على الأقل)', 'class': 'form-input-glass'}),
        label='كلمة المرور'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'تأكيد كلمة المرور', 'class': 'form-input-glass'}),
        label='تأكيد كلمة المرور'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'academic_id', 'department']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'اسم المستخدم (باللغة الإنجليزية)', 'class': 'form-input-glass'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'الاسم الأول', 'class': 'form-input-glass'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'اسم العائلة', 'class': 'form-input-glass'}),
            'email': forms.EmailInput(attrs={'placeholder': 'البريد الإلكتروني الجامعي أو الشخصي', 'class': 'form-input-glass'}),
            'academic_id': forms.TextInput(attrs={'placeholder': 'الرقم الجامعي (مثلاً: CS-2022-045)', 'class': 'form-input-glass'}),
            'department': forms.TextInput(attrs={'placeholder': 'القسم أو الكلية (مثلاً: علوم الحاسوب)', 'class': 'form-input-glass'}),
        }
        labels = {
            'username': 'اسم المستخدم',
            'first_name': 'الاسم الأول',
            'last_name': 'اسم العائلة',
            'email': 'البريد الإلكتروني',
            'academic_id': 'الرقم الجامعي',
            'department': 'القسم / التخصص',
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', 'كلمتا المرور غير متطابقتين.')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'اسم المستخدم', 'class': 'form-input-glass'}),
        label='اسم المستخدم'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'كلمة المرور', 'class': 'form-input-glass'}),
        label='كلمة المرور'
    )
