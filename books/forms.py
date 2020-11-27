from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Ureg
from django import forms

# class OrderForm(ModelForm):
# 	class Meta:
# 		model = Order
# 		fields = '__all__'

class RegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('email', 'first_name', 'last_name', 'username')
		# fields = ['firstName','lastName','username', 'email', 'password', 'confirmPassword',
		#        'phoneNumber','cardNumber','address'
		# 	   ]

	# def clean_email(self):
	# 	email = self.cleaned_data.get('email')
	# 	qs = User.objects.filter(email=email)
	# 
	# 	if qs.exists():
	# 		raise UserCreationForm.ValidationError("email is taken already")
	# 	return email



