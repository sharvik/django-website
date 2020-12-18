from django import forms
from django.contrib.auth.forms import UserCreationForm

from myapp.models import Order, Review, Student


class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False, label="Student Name")
    length = forms.TypedChoiceField(widget=forms.RadioSelect,
                                    choices=LENGTH_CHOICES, coerce=int, required=False)
    max_price = forms.IntegerField(label="Maximum Price", min_value=0)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(),
                   'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name', }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'courses': forms.RadioSelect()}
        labels = {'reviewer': 'Please enter a valid email', 'rating': 'Rating: An integer between 1 (worst) and 5 ('
                                                                      'best)'}


class RegisterForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ['user_image', 'username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'level', 'address', 'province', 'registered_courses',
                  'interested_in']
