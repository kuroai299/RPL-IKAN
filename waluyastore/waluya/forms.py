from django import forms
from .models import Fish, FishMedicine, AquariumStuff, FishFood
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class FishForm(forms.ModelForm):
    class Meta:
        model = Fish
        fields = ['name', 'description', 'price', 'stock', 'image', 'size', 'color']

class FishMedicineForm(forms.ModelForm):
    class Meta:
        model = FishMedicine
        fields = ['name', 'description', 'price', 'stock', 'image', 'medicine_type']

class AquariumStuffForm(forms.ModelForm):
    class Meta:
        model = AquariumStuff
        fields = ['name', 'description', 'price', 'stock', 'image', 'stuff_type']

class FishFoodForm(forms.ModelForm):
    class Meta:
        model = FishFood
        fields = ['name', 'description', 'price', 'stock', 'image', 'food_type']

from django import forms

class AdminLoginForm(forms.Form):
    email = forms.EmailField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)

    # Jika Anda ingin menambahkan validasi custom
    def clean_email(self):
        email = self.cleaned_data['email']
        return email


# Form untuk sign-up user biasa
class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, help_text="Password must be at least 8 characters.")  # Password minimal 8 karakter

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Hanya username, email, dan password

    # Custom clean untuk memvalidasi email agar unik
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Periksa apakah email sudah ada di database
            raise forms.ValidationError("Email is already taken. Please use a different email.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Enkripsi password
        if commit:
            user.save()  # Simpan data pengguna ke database
        return user